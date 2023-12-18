<script lang="ts">
    import {ListBox, ListBoxItem} from "@skeletonlabs/skeleton";
    import {choose} from "$lib/ToneSelector";

    type Style = {
        display: string,
        variant: string[][],
    };
    const styles: Record<string, Style> = {
        "classical": {
            display: "Classical",
            variant: [["Allegro", "Allegro"], ["Moderato", "Moderato"], ["Andante", "Andante"]],
        },
        "pop": {
            display: "Pop",
            variant: [],
        },
        "folk": {
            display: "Folk",
            variant: [],
        },
        "hiphop": {
            display: "Hiphop",
            variant: [["boombap", "Boombap"], ["drill", "Drill"], ["trap", "Trap"]],
        }
    };
    let selectedStyle = ""; // selected music style
    let selectedVar = ""; // selected variant

    // Clear selected variant when selected style change
    $: selectedStyle, selectedVar = "";
    $: if(selectedVar === "random") {
        selectedVar = choose(styles[selectedStyle].variant)[0]
    }

    export let style = "";
    $: style = (
        (!!styles[selectedStyle]
            && Array.isArray(styles[selectedStyle].variant)
            && styles[selectedStyle].variant.length <= 0)
        || selectedVar !== ""
    ) ? (selectedStyle + ((!!selectedVar) ? ("::" + selectedVar) : "")) : "";

</script>

<div>
    <div class="grid grid-cols-2 gap-4">
        <div class="select">
            <ListBox>
                {#each Object.entries(styles) as [val, style]}
                    <ListBoxItem bind:group={selectedStyle} name="style" value={val}>{style.display}</ListBoxItem>
                {/each}
            </ListBox>
        </div>
        {#if !!styles[selectedStyle] && Array.isArray(styles[selectedStyle].variant) && styles[selectedStyle].variant.length}
            <div class="select">
                <ListBox>
                    <ListBoxItem bind:group={selectedVar} name="style" value="random">Random</ListBoxItem>
                    {#each styles[selectedStyle].variant as [val, variant]}
                        <ListBoxItem bind:group={selectedVar} name="style" value={val}>{variant}</ListBoxItem>
                    {/each}
                </ListBox>
            </div>
        {/if}
    </div>
</div>