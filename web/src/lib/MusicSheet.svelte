<style>
    .at-wrap {
        width: 80vw;
        height: 80vh;
        margin: 0 auto;
        border: 1px solid rgba(0, 0, 0, 0.12);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        position: relative;
    }

    .at-content {
        position: relative;
        overflow: hidden;
        flex: 1 1 auto;
    }

    /** Sidebar (now with hover expansion) **/
    .at-sidebar {
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        max-width: 70px;
        width: auto;
        display: flex;
        align-content: stretch;
        z-index: 1001;
        overflow: hidden;
        border-right: 1px solid rgba(0, 0, 0, 0.12);
        background: #f7f7f7;
    }

    .at-sidebar:hover {
        max-width: 400px;
        transition: max-width 0.2s;
        overflow-y: auto;
    }

    /** Track selector **/
    .at-track {
        display: flex;
        position: relative;
        padding: 5px;
        transition: background 0.2s;
        cursor: pointer;
    }

    .at-track:hover {
        background: rgba(0, 0, 0, 0.1);
    }

    .at-track > .at-track-icon,
    .at-track > .at-track-details {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .at-track > .at-track-icon {
        flex-shrink: 0;
        font-size: 32px;
        opacity: 0.5;
        transition: opacity 0.2s;
        width: 64px;
        height: 64px;
        margin-right: 5px;
        align-items: center;
    }

    .at-track-name {
        font-weight: bold;
        margin-bottom: 5px;
    }

    .at-track:hover > .at-track-icon {
        opacity: 0.8;
    }

    .at-track.active {
        background: rgba(0, 0, 0, 0.03);
    }

    .at-track.active > .at-track-icon {
        color: #4972a1;
        opacity: 1;
    }

    .at-track > .at-track-name {
        font-weight: 500;
    }

    /** Footer **/
    .at-controls {
        flex: 0 0 auto;
        display: flex;
        justify-content: space-between;
        background: #436d9d;
        color: #fff;
    }

    .at-controls > div {
        display: flex;
        justify-content: flex-start;
        align-content: center;
        align-items: center;
    }

    .at-controls > div > * {
        display: flex;
        text-align: center;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        padding: 4px;
        margin: 0 3px;
    }

    .at-controls .btn {
        color: #fff;
        border-radius: 0;
        height: 40px;
        width: 40px;
        height: 40px;
        font-size: 16px;
    }

    .at-controls a.active {
        background: #5588c7;
        text-decoration: none;
    }

    .at-controls .btn i {
        vertical-align: top;
    }

    .at-controls select {
        -moz-appearance: none;
        -webkit-appearance: none;
        appearance: none;
        border: none;
        width: 100%;
        height: 40px;
        background: #436d9d;
        padding: 4px 10px;
        color: #fff;
        font-size: 16px;
        text-align-last: center;
        text-align: center;
        -ms-text-align-last: center;
        -moz-text-align-last: center;
        cursor: pointer;
    }

    .at-song-title {
        font-weight: bold;
    }
</style>

<script lang="ts">
    import type {AlphaTabApi} from "$lib/alphaTab";
    import Fa from 'svelte-fa'
    import {faEdit, faGuitar, faHourglassHalf, faPrint, faRetweet, faSearch} from "@fortawesome/free-solid-svg-icons";

    export let file: File;
    let wrapper: HTMLElement;
    let score;
    let api: AlphaTabApi;
    let trackArr = [];
    let trackEnable: Map<number, boolean> = new Map();

    function createAlphaTab(domObj: HTMLElement) {
        if (!(window as any).alphaTab) return;
        const alphaTab: typeof import('./alphaTab') = (window as any).alphaTab;
        api = new alphaTab.AlphaTabApi(domObj, {
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
                soundFont: `https://cdn.jsdelivr.net/npm/@coderline/alphatab@alpha/dist/soundfont/sonivox.sf2`
            }
        });

        api.scoreLoaded.on((score) => {
            trackArr = score.tracks;
        });

        api.renderStarted.on(() => {
            console.log("Render Started");
            // collect tracks being rendered
            const tracks = api.tracks.map((t) => t.index);
            trackArr.forEach((t) => {
                trackEnable.set(t.index, tracks.includes(t.index))
            });
        });

        (async () => {
            const data = await file.arrayBuffer()
            const score = alphaTab.importer.ScoreLoader.loadScoreFromBytes(new Uint8Array(data));
            api.renderScore(score);
            api.render();
        })()


    }


</script>

<div class="bg-white">
    <div class="at-wrap" bind:this={wrapper}>
        <div class="at-content">
            <div class="at-sidebar">
                <div class="at-sidebar-content">
                    <div class="at-track-list">
                        {#each trackArr as track}
                            <div class="at-track" class:active={trackEnable.get(track.index)}
                                 on:click|self={api.renderTracks([track])}>
                                <div class="at-track-icon">
                                    <Fa icon={faGuitar}/>
                                </div>
                                <div class="at-track-details">
                                    <div class="at-track-name">{track.name}</div>
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>
            </div>
            <div class="at-viewport">
                <div class="at-main" use:createAlphaTab></div>
            </div>
        </div>
        <div class="at-controls">
            <div class="at-controls-left">
                <div class="at-song-info">
                    <span class="at-song-title"></span> -
                    <span class="at-song-artist"></span>
                </div>
            </div>
            <div class="at-controls-right">
                <a class="btn toggle at-count-in">
                    <Fa icon={faHourglassHalf}/>
                </a>
                <a class="btn toggle at-metronome">
                    <Fa icon={faEdit}/>
                </a>
                <a class="btn toggle at-loop">
                    <Fa icon={faRetweet}/>
                </a>
                <a class="btn at-print">
                    <Fa icon={faPrint}/>
                </a>
                <div class="at-zoom">
                    <Fa icon={faSearch}/>
                    <select>
                        <option value="25">25%</option>
                        <option value="50">50%</option>
                        <option value="75">75%</option>
                        <option value="90">90%</option>
                        <option value="100" selected>100%</option>
                        <option value="110">110%</option>
                        <option value="125">125%</option>
                        <option value="150">150%</option>
                        <option value="200">200%</option>
                    </select>
                </div>
                <div class="at-layout">
                    <select>
                        <option value="horizontal">Horizontal</option>
                        <option value="page" selected>Page</option>
                    </select>
                </div>
            </div>
        </div>
    </div>
</div>