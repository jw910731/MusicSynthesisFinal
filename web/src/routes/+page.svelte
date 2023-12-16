<script lang="ts">
    import {getToastStore} from "@skeletonlabs/skeleton";
    import type {ToastSettings} from "@skeletonlabs/skeleton";
    import MusicSelector from "$lib/MusicSelector.svelte";
    import MusicSheet from "$lib/MusicSheet.svelte";

    const toastStore = getToastStore();
    let scoreFile: File | null = null;

    async function generateMusic(tone: string, style: string) {
        const req_data = {tone, style}
        const raw_resp = await fetch("/api/generate", {
            method: "POST",
            body: JSON.stringify(req_data)
        })
        if (raw_resp.status == 200) {
            const data = await raw_resp.blob();
            scoreFile = new File([data], "music21.musicxml")
        } else {

            let msg: string;
            if (raw_resp.status == 400) {
                const text = await raw_resp.text();
                try {
                    const json = JSON.parse(text);
                    msg = json["err"]["msg"]
                    console.error(json["err"]["detail"])
                } catch (e) {
                    msg = text;
                }
            } else {
                msg = `${raw_resp.status} ${raw_resp.statusText}`;
            }
            const toast: ToastSettings = {
                message: msg,
                background: "variant-filled-error",
            };
            toastStore.trigger(toast);
        }
    }
</script>

<div class="container mx-auto">
    <MusicSelector callback={generateMusic}/>
    {#if !!scoreFile}
        <MusicSheet file={scoreFile}/>
    {/if}
</div>