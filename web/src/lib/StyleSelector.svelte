<script lang="ts">
    import {ListBox, ListBoxItem} from "@skeletonlabs/skeleton";

    type Style = {
        display: string,
        variant: string[],
    };
    const styles: Record<string, Style> = {
        "classical": {
            display: "Classical",
            variant: ["Allegro", "Moderato", "Andante"],
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
            variant: ["Boombap", "Drill", "Trap"],
        }
    };
    let selectedStyle = ""; // selected music style
    let selectedVar = ""; // selected variant

    // Clear selected variant when selected style change
    $: selectedStyle, selectedVar = "";

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
                {#each Object.entries(styles) as [key, style]}
                    <ListBoxItem bind:group={selectedStyle} name="style" value={key}>{style.display}</ListBoxItem>
                {/each}
            </ListBox>
        </div>
        <div class="select">
            {#if !!styles[selectedStyle] && Array.isArray(styles[selectedStyle].variant) && styles[selectedStyle].variant.length}
                <ListBox>
                    {#each styles[selectedStyle].variant as variant}
                        <ListBoxItem bind:group={selectedVar} name="style" value={variant}>{variant}</ListBoxItem>
                    {/each}
                </ListBox>
            {/if}
        </div>
    </div>
</div>