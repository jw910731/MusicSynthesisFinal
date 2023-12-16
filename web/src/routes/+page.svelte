<script lang="ts">
    import ToneSelector from "$lib/ToneSelector.svelte";
    import StyleSelector from "$lib/StyleSelector.svelte";
    import {ProgressRadial} from "@skeletonlabs/skeleton";
    import MusicSelector from "$lib/MusicSelector.svelte";

    async function generateMusic(tone: string, style: string) {
        console.log(tone, style);
    }
</script>

<div class="container mx-auto">
    <MusicSelector callback={generateMusic} />
</div>