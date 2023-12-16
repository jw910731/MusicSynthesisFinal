<script lang="ts">
    import ToneSelector from "./ToneSelector.svelte";
    import StyleSelector from "./StyleSelector.svelte";
    import {ProgressRadial} from "@skeletonlabs/skeleton";

    let tone = "";
    let style = "";
    let disableSubmit = false;
    export let callback: (tone: string, style: string)=>Promise<void>;

    async function cbHandler() {
        disableSubmit = true;
        await callback(tone, style);
        disableSubmit = false;
    }
</script>


<div class="grid grid-cols-2 gap-2">
    <div>
        <p class="my-2">Tone Selection: </p>
        <ToneSelector bind:tone/>
        <p>Tone: {tone}</p>
    </div>
    <div>
        <p class="my-2">Style: </p>
        <StyleSelector bind:style/>
        <p>Style: {style}</p>
        <button type="button" class="btn variant-filled-primary" on:click={cbHandler} disabled={disableSubmit}>
            {#if disableSubmit}
                <ProgressRadial width="w-4"/>
            {:else}
                <p>Generate Music!</p>
            {/if}
        </button>
    </div>
</div>
