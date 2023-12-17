<style>
    :global(.at-cursor-bar) {
        /* Defines the color of the bar background when a bar is played */
        background: rgba(255, 242, 0, 0.25);
    }

    :global(.at-selection div) {
        /* Defines the color of the selection background */
        background: rgba(64, 64, 255, 0.1);
    }

    :global(.at-cursor-beat) {
        /* Defines the beat cursor */
        background: rgba(64, 64, 255, 0.75);
        width: 3px;
    }

    :global(.at-highlight *) {
        /* Defines the color of the music symbols when they are being played (svg) */
        fill: #0078ff;
        stroke: #0078ff;
    }
</style>

<script lang="ts">
    import type {AlphaTabApi} from "$lib/alphaTab";
    import Fa from 'svelte-fa'
    import {faPause, faPlay, faStepBackward} from "@fortawesome/free-solid-svg-icons";
    import {onDestroy, onMount} from "svelte";
    import {ProgressBar} from "@skeletonlabs/skeleton";

    export let file: Blob;

    let wrapper: HTMLElement;
    let scrollElement: HTMLElement;
    let sheetElement: HTMLElement;

    let score;
    let api: AlphaTabApi;
    let trackArr = [];
    let trackEnable: Map<number, boolean> = new Map();
    let percentage: number;
    let playerReady: boolean;
    let playing: boolean;
    let playTime = [0, 0];
    let artist = "", title = "";

    function formatDuration(milliseconds: number) {
        let seconds = milliseconds / 1000;
        const minutes = (seconds / 60) | 0;
        seconds = (seconds - minutes * 60) | 0;
        return (
            String(minutes).padStart(2, "0") +
            ":" +
            String(seconds).padStart(2, "0")
        );
    }


    function createAlphaTab() {
        if (!(window as any).alphaTab) return;
        const alphaTab: typeof import('./alphaTab') = (window as any).alphaTab;
        api = new alphaTab.AlphaTabApi(sheetElement, {
            core: {
                engine: "html5",
                useWorkers: true,
                tracks: "all",
            },
            display: {
                staveProfile: 'Default'
            },
            player: {
                enablePlayer: true,
                enableUserInteraction: true,
                enableCursor: true,
                soundFont: `https://cdn.jsdelivr.net/npm/@coderline/alphatab@alpha/dist/soundfont/sonivox.sf2`,
                scrollElement: scrollElement,
            }
        });

        api.scoreLoaded.on((score) => {
            trackArr = score.tracks;
            artist = score.artist;
            title = score.title;
        });
        api.renderStarted.on(() => {
            console.log("Render Started");
            // collect tracks being rendered
            const tracks = api.tracks.map((t) => t.index);
            trackArr.forEach((t) => {
                trackEnable.set(t.index, tracks.includes(t.index))
            });
        });
        api.playerReady.on(() => {
            playerReady = true;
        });
        api.playerStateChanged.on((e) => {
            playing = e.state === alphaTab.synth.PlayerState.Playing;
        });
        let previousTime: number;
        api.playerPositionChanged.on((e) => {
            // reduce number of UI updates to second changes.
            const currentSeconds = (e.currentTime / 1000) | 0;
            if (currentSeconds == previousTime) {
                return;
            }
            percentage = Math.round((e.currentTime / e.endTime) * 100);
            playTime = [e.currentTime, e.endTime];
        });


        (async () => {
            const data = await file.arrayBuffer()
            const score = alphaTab.importer.ScoreLoader.loadScoreFromBytes(new Uint8Array(data));
            api.renderScore(score);
            api.renderTracks(score.tracks);
        })()
    }

    onMount(createAlphaTab);
    onDestroy(() => {
        api.destroy();
    })
</script>

<div class="dark:bg-white">
    <div class="border-black border-2 h-screen flex relative flex-col overflow-hidden" bind:this={wrapper}>
        <div class="relative overflow-hidden flex-auto">
            <div class="overflow-y-auto absolute top-0 left-20 right-0 bottom-0 p-5" bind:this={scrollElement}>
                <div bind:this={sheetElement}></div>
            </div>
        </div>
        <div class="flex-grow-0 flex-shrink-0 flex justify-between bg-blue-500">
            <div class="flex justify-start content-center items-center">
                <a role="button" class="decoration-0 text-surface-50 dark:text-surface-900 border-r-0 h-10 w-10 text-base flex text-center items-center justify-center cursor-pointer p-1 my-0.5 mx-0"
                   class:disabled={!playerReady}>
                    <Fa icon={faStepBackward}/>
                </a>
                <a role="button" class="decoration-0 text-surface-50 dark:text-surface-900 border-r-0 h-10 w-10 text-base flex text-center items-center justify-center cursor-pointer p-1 my-0.5 mx-0"
                   class:disabled={!playerReady} on:click={()=> api.playPause()}>
                    {#if playing}
                        <Fa icon={faPause}/>
                    {:else}
                        <Fa icon={faPlay}/>
                    {/if}
                </a>
            </div>
            <div class="flex-auto flex items-center justify-center">
                {#if playerReady}
                    <ProgressBar value={percentage} max={100}/>
                {/if}
            </div>
            <div class="flex justify-start content-center items-center">
                <div class="at-song-info flex text-center items-center justify-center cursor-pointer p-1 my-0.5 mx-0 text-surface-50 dark:text-surface-900">
                    <span class="font-bold">{title}</span> -
                    <span>{artist}</span>
                </div>
                <div class="text-surface-50 dark:text-surface-900 flex text-center items-center justify-center cursor-pointer p-1 my-0.5 mx-0">{playTime.map(formatDuration).join("/")}</div>
            </div>
        </div>
    </div>
</div>
