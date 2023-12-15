<script>
    import {ListBox, ListBoxItem} from '@skeletonlabs/skeleton';
    import {ToneState, choose} from './utils';

    const notes = ["C", "D", "E", "F", "G", "A", "B"];
    const accidentals = [
        ["#", "#"],
        ["", "♮"],
        ["-", "♭"]
    ];
    const types = [
        [ToneState.Major, "Major"],
        [ToneState.Minor, "Minor"]
    ]
    let selectedNote = "C";
    let selectedAccidental = "";
    let selectedType = ToneState.Major;

    export let tone = "C";
    $: tone = (() => {
        if (selectedNote === "random") {
            selectedNote = choose(notes);
        }
        if (selectedAccidental === "random") {
            selectedAccidental = choose(accidentals)[0];
        }
        if (selectedType === ToneState.Major) {
            return selectedNote + selectedAccidental;
        } else {
            return (selectedNote + selectedAccidental).toLowerCase();
        }
    })();
</script>
<div>
    <div class="grid grid-cols-12 gap-4">
        <div class="select col-span-2">
            <ListBox size="4">
                <ListBoxItem bind:group={selectedNote} name="note" value="random">Random</ListBoxItem>
                {#each notes as note}
                    <ListBoxItem bind:group={selectedNote} name="note" value={note}>{note}</ListBoxItem>
                {/each}
            </ListBox>
        </div>
        <div class="select col-span-2">
            <ListBox size="4">
                <ListBoxItem bind:group={selectedAccidental} name="accidental" value="random">Random</ListBoxItem>
                {#each accidentals as [val, display]}
                    <ListBoxItem bind:group={selectedAccidental} name="accidental" value={val}>{display}</ListBoxItem>
                {/each}
            </ListBox>
        </div>
        <div class="select col-span-2">
            <ListBox size="1">
                {#each types as [val, display]}
                    <ListBoxItem bind:group={selectedType} name="type" value={val}>{display}</ListBoxItem>
                {/each}
            </ListBox>
        </div>
    </div>
</div>