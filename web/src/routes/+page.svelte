<script>
    import ToneSelector from "$lib/ToneSelector.svelte";
    import StyleSelector from "$lib/StyleSelector.svelte";
    import {ProgressRadial} from "@skeletonlabs/skeleton";

    let tone = "";
    let style = "";
</script>

<div class="container mx-auto">
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
        </div>
    </div>
</div>