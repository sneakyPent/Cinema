<template>
    <div>

    </div>
</template>

<script>


export default {

    name: 'Logout',
    mounted: function () {
        this.$session.destroy();
        window.location.reload(true);
    },
}
</script>
