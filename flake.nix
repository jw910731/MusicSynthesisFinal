{
  inputs = {
    nixpkgs.url = "github:cachix/devenv-nixpkgs/rolling";
    nixpkgs-upstream.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    systems.url = "github:nix-systems/default";
    devenv.url = "github:cachix/devenv";
    devenv.inputs.nixpkgs.follows = "nixpkgs";
    nixpkgs-python.url = "github:cachix/nixpkgs-python";
    nixpkgs-python.inputs.nixpkgs.follows = "nixpkgs";

    poetry2nix.url = "github:nix-community/poetry2nix";
    poetry2nix.inputs.nixpkgs.follows = "nixpkgs";
    pnpm2nix.url = "github:jw910731/pnpm2nix-nzbr";
    pnpm2nix.inputs.nixpkgs.follows = "nixpkgs";
  };

  nixConfig = {
    extra-trusted-public-keys = "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw=";
    extra-substituters = "https://devenv.cachix.org";
  };

  outputs = { self, nixpkgs, nixpkgs-upstream, devenv, systems, poetry2nix, pnpm2nix, ... } @ inputs:
    let
      forEachSystem = nixpkgs.lib.genAttrs (import systems);
      targetOverlays = final: prev: {
        musl = prev.musl.overrideAttrs (old: {
          patches = (old.patches or []) ++ (prev.lib.optional (prev.stdenv.buildPlatform.isDarwin) (builtins.fetchurl {
              url = "https://github.com/timbertson/musl/compare/f314e133929b6379eccc632bef32eaebb66a7335...05b89f783fd1873ce9ec1127fa76d002921caa23.patch";
              sha256 = "1n17lawfpd551707nh3pr6ilyh0qh7rh0vdb522ijdygggh49rhd";
            })
          );
        });
        giflib = prev.musl.overrideAttrs (old: {
          postPatch = (old.postPatch or "") + (prev.lib.optionalString (prev.stdenv.buildPlatform.isDarwin && prev.stdenv.hostPlatform.isLinux) "sed -i 's|$(shell uname)|Linux|g' Makefile");
        });
        tcl = prev.tcl.overrideAttrs (old: {
          nativeBuildInputs = (old.nativeBuildInputs or []) ++ [ prev.deterministic-host-uname ];
        });
        openblas = prev.openblas.overrideAttrs (old: {
          makeFlags = (old.makeFlags or []) ++ ((prev.lib.mapAttrsToList (var: val: "${var}=${(val: if !builtins.isBool val then toString val else if val then "1" else "0") val}")) {
            LDFLAGS = "-Wl,-rpath-link,${prev.lib.getLib prev.buildPackages.gfortran.cc}/lib";
          });
          preBuild = (old.preBuild or "") + prev.lib.optionalString (prev.stdenv.hostPlatform.isx86_64) ''
            makeFlagsArray+=(CFLAGS="-msse3 -march=x86-64-v3")
          '';
          nativeBuildInputs = (old.nativeBuildInputs or []) ++ [ prev.deterministic-host-uname ];
        });
        boost = let arch = {
              "aarch64" = "arm";
              "x86_64" = "x86_64";
            }.${prev.stdenv.hostPlatform.parsed.cpu.name};
            python = prev.python311;
            in (prev.boost.override {
              inherit python;
              enablePython = true;
            }).overrideAttrs (old: {
          preConfigure = (old.preConfigure or "") + prev.lib.optionalString (prev.stdenv.hostPlatform.system != prev.stdenv.buildPlatform.system) ''
            ${prev.buildPackages.perl}/bin/perl -i -0777 -pe 's!using (gcc|clang) : cross!using \1 : ${arch}!g ; s!using python : :([^;]+);!using python : ${python.pythonVersion} :\1: <target-os>linux \n      ;!g' user-config.jam
          '';
          nativeBuildInputs = (old.nativeBuildInputs or []) ++ [ prev.deterministic-host-uname ];
        });
      };
    in
    {
      packages = forEachSystem (system: 
      let
        pkgs = import nixpkgs { inherit system; };
        pnpm2nix' = pnpm2nix.packages.${system};
        lib = pkgs.lib;
        mkLinuxPkgs = arch: import nixpkgs-upstream { inherit system; crossSystem.config = "${arch}-unknown-linux-musl"; overlays = [targetOverlays poetry2nix.overlays.default]; };
        archName = {
          "x86_64" = "amd64";
          "aarch64" = "arm64";
        };
        frontend = pnpm2nix'.mkPnpmPackage {
          src = with lib.fileset; toSource {
            root = ./web;
            fileset = intersection (gitTracked ./.) ./web;
          };
          nodejs = pkgs.nodejs_18;
          pnpm = pkgs.nodejs_18.pkgs.pnpm;
          distDir = "build";
          copyPnpmStore = true;
        };
        backend = linuxPkgs: let
          inherit (linuxPkgs.poetry2nix) mkPoetryApplication overrides;
          python = linuxPkgs.python311;
        in mkPoetryApplication {
          inherit python;
          projectDir = with lib.fileset; toSource {
            root = ./.;
            fileset = unions [
              ./src
              ./poetry.lock
              ./pyproject.toml
              ./README.md
            ];
          };
          preferWheels = true;
          overrides = overrides.withDefaults (self: super: let 
          cmakeFlags' = with super.lib; with super;
            optionals (stdenv.hostPlatform != stdenv.buildPlatform) ([
              "-DCMAKE_SYSTEM_NAME=${findFirst isString "Generic" (optional (!stdenv.hostPlatform.isRedox) stdenv.hostPlatform.uname.system)}"
            ] ++ optionals (stdenv.hostPlatform.uname.processor != null) [
              "-DCMAKE_SYSTEM_PROCESSOR=${stdenv.hostPlatform.uname.processor}"
            ] ++ optionals (stdenv.hostPlatform.uname.release != null) [
              "-DCMAKE_SYSTEM_VERSION=${stdenv.hostPlatform.uname.release}"
            ] ++ optionals (stdenv.hostPlatform.isDarwin) [
              "-DCMAKE_OSX_ARCHITECTURES=${stdenv.hostPlatform.darwinArch}"
            ] ++ optionals (stdenv.buildPlatform.uname.system != null) [
              "-DCMAKE_HOST_SYSTEM_NAME=${stdenv.buildPlatform.uname.system}"
            ] ++ optionals (stdenv.buildPlatform.uname.processor != null) [
              "-DCMAKE_HOST_SYSTEM_PROCESSOR=${stdenv.buildPlatform.uname.processor}"
            ] ++ optionals (stdenv.buildPlatform.uname.release != null) [
              "-DCMAKE_HOST_SYSTEM_VERSION=${stdenv.buildPlatform.uname.release}"
            ] ++ optionals (stdenv.buildPlatform.canExecute stdenv.hostPlatform) [
              "-DCMAKE_CROSSCOMPILING_EMULATOR=env"
            ] ++ optionals stdenv.hostPlatform.isStatic [
              "-DCMAKE_LINK_SEARCH_START_STATIC=ON"
            ]);
          in {
            music21 = super.music21.overridePythonAttrs (old: {
              buildInputs = old.buildInputs or [] ++ [super.hatchling];
            });
            pybind11 = super.pybind11.overridePythonAttrs (old: {
              env."CMAKE_ARGS" = builtins.concatStringsSep " " (old.cmakeFlags ++ [
                "-DCMAKE_C_COMPILER=${super.stdenv.cc.targetPrefix}cc"
                "-DCMAKE_CXX_COMPILER=${super.stdenv.cc.targetPrefix}c++"
                "-DCMAKE_AR=${super.stdenv.cc.targetPrefix}ar"
                "-DCMAKE_RANLIB=${super.stdenv.cc.targetPrefix}ranlib"
                "-DCMAKE_STRIP=${super.stdenv.cc.targetPrefix}strip"
              ] ++ cmakeFlags');
            });
            matplotlib = (super.matplotlib.override {
              enableTk = false;
              python = super.pythonOnBuildForHost.interpreter;
            }).overridePythonAttrs (old: let 
                parsed = super.stdenv.targetPlatform.parsed;
              in {
              preBuild = (lib.optionalString (lib.hasSuffix ".tar.gz" old.src) ''
                sed -ie 's!sys.platform!"${parsed.kernel.name}"!g ; s!import numpy as np!!g ; s!np.get_include()!"${super.numpy}/lib/python${python.pythonVersion}/site-packages/numpy/core/include"!g' setupext.py
              '' + (old.preBuild or ""));
              env = (old.env or {}) // {
                "CC" = "${super.stdenv.cc.targetPrefix}cc";
                "CXX" = "${super.stdenv.cc.targetPrefix}c++";
                "AR" = "${super.stdenv.cc.targetPrefix}ar";
                "RANLIB" = "${super.stdenv.cc.targetPrefix}ranlib";
                "STRIP" = "${super.stdenv.cc.targetPrefix}strip";

                # Extreme hack to get matplotlib cross compile on darwin
                # Caused by Pybind11Extension, see more at below link
                # https://github.com/pybind/pybind11/blob/66c3774a6402224b1724329c81c880e76633a92b/pybind11/setup_helpers.py#L191
                "MACOSX_DEPLOYMENT_TARGET" = super.lib.optionalString (super.stdenv.hostPlatform.isDarwin) "10.99";
              };
              pipBuildFlags = [
                "-C plat-name=${parsed.kernel.name}-${parsed.cpu.name}"
              ];
            });
          });
        };
        docker = linuxPkgs: pkgs.dockerTools.buildLayeredImage {
          name = "registry.h.jw910731.dev/nix/music-synth-web";
          tag = "0.1.0-" + archName.${linuxPkgs.stdenv.hostPlatform.parsed.cpu.name};
          contents = [
            (backend linuxPkgs).dependencyEnv
            linuxPkgs.busybox
          ];
          config = {
            Entrypoint = [ "/bin/web" ];
            Env = [
              "FLASK_SERVER_NAME=0.0.0.0:8000"
              "FLASK_ENV=production"
              "BASE_DIR=${frontend}"
            ];
            WorkingDir = "/";
          };
          created = "now";
          maxLayers = 127;
        };
      in {
        devenv-up = self.devShells.${system}.default.config.procfileScript;
        docker = (docker (mkLinuxPkgs pkgs.stdenv.hostPlatform.parsed.cpu.name));
        web = frontend;
      } // (lib.mapAttrs' (name: value: lib.nameValuePair ("docker-${(archName.${name})}") value) (lib.genAttrs ["x86_64" "aarch64"] (e: (docker (mkLinuxPkgs e)))))
      );

      devShells = forEachSystem
        (system:
          let
            pkgs = nixpkgs.legacyPackages.${system};
          in
          {
            default = devenv.lib.mkShell {
              inherit inputs pkgs;
              modules = [
                {
                  # https://devenv.sh/reference/options/
                  packages = [ ];
                  languages.python = {
                    enable = true;
                    version = "3.11";
                    poetry = {
                      enable = true;
                      activate.enable = true;
                      install.enable = true;
                      install.compile = true;
                    };
                  };
                  languages.javascript = {
                    enable = true;
                    package = pkgs.nodejs-slim_18;
                    corepack.enable = true;
                    directory = "web";
                    pnpm = {
                      enable = true;
                      install.enable = true;
                    };
                  };
                }
              ];
            };
          });
    };
}
