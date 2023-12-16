<script>
    import "../app.postcss";
    import {autoModeWatcher, AppShell, AppBar, LightSwitch, initializeStores, Toast} from '@skeletonlabs/skeleton';

    initializeStores();

</script>

<svelte:head>
    {@html `<script>${autoModeWatcher.toString()} autoModeWatcher();</script>`}
</svelte:head>

<Toast />
<AppShell>
    <svelte:fragment slot="header">
        <AppBar>
            <svelte:fragment slot="lead">
                <h3 class="h3 mr-auto"> Music and Sound Synthesis Final Project </h3>
            </svelte:fragment>
            <svelte:fragment slot="trail">
                <LightSwitch/>
            </svelte:fragment>
        </AppBar>
    </svelte:fragment>
    <!-- (sidebarLeft) -->
    <!-- (sidebarRight) -->
    <!-- (pageHeader) -->
    <!-- Router Slot -->
    <slot/>
    <!-- ---- / ---- -->
    <!-- (pageFooter) -->
    <!-- (footer) -->
</AppShell>