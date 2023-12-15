<script>
    import ToneSelector from "./ToneSelector.svelte";

    let tone = "";
</script>

<div class="container mx-auto">
    <div>
        <p class="my-2">Tone Selection: </p>
        <ToneSelector bind:tone />
        <p>Tone: {tone}</p>
    </div>
</div>