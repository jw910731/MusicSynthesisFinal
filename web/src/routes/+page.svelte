<script lang="ts">
    import {getToastStore} from "@skeletonlabs/skeleton";
    import type {ToastSettings} from "@skeletonlabs/skeleton";
    import MusicSelector from "$lib/MusicSelector.svelte";
    import MusicSheet from "$lib/MusicSheet.svelte";
    import Fa from "svelte-fa";
    import {faDownload} from "@fortawesome/free-solid-svg-icons";

    const toastStore = getToastStore();
    let scoreFile: Blob | null = null;

    $: fileLink = ((!!scoreFile) ? (URL.createObjectURL(scoreFile)) : "");

    async function generateMusic(tone: string, style: string) {
        const req_data = {tone, style}
        const raw_resp = await fetch("/api/generate", {
            method: "POST",
            body: JSON.stringify(req_data)
        })
        if (raw_resp.status == 200) {
            scoreFile = await raw_resp.blob();
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
    <div class="my-2">
        <MusicSelector callback={generateMusic}/>
    </div>
    {#if !!scoreFile}
        <div class="my-2">
            <a type="button" class="btn variant-filled-success text-surface-50 mt-2 mb-4" href={fileLink} download="music.xml">
                <Fa class="mr-2" icon="{faDownload}"/>
                Download music sheet
            </a>
            <MusicSheet file={scoreFile}/>
        </div>
    {/if}
</div>