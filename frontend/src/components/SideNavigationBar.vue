<template>
    <mdb-side-nav-2
        v-if="loaded"
        :value="true"
        :data="navops"
        side
        slim
        expand-on-hover
        :slim-collapsed="slimCollapsed"
        @toggleSlim="slimCollapsed = $event"
        sidenav-class="grey"
        color="white"
    >
        <div slot="header">
            <div
                class="d-flex align-items-center my-4"
                :class="'justify-content-center'"
            >
                <mdb-avatar :width="slimCollapsed ? 40 : 80" style="flex: 0 0 auto">
                    <img
                        src="https://mdbootstrap.com/img/Photos/Avatars/avatar-1.jpg"
                        class="img-fluid rounded-circle z-depth-3"
                    />
                </mdb-avatar>
            </div>
            <div
                class="d-flex align-items-center my-4"
                :class="'justify-content-center'"
            >
                <p
                    class="m-t mb-0 ml-4 p-0"
                    style="flex: 0 2 auto"
                    v-show="!slimCollapsed"
                >
                    <strong
                    ><h6 class="plan-cost white-text">
                        {{ this.userData.username }}</h6>
                    </strong>
                </p>
            </div>
            <div
                class="d-flex align-items-center my-4"
                :class="'justify-content-center'"
            >
                <p
                    class="m-t mb-0 ml-4 p-0"
                    style="flex: 0 2 auto"
                    v-show="!slimCollapsed"
                >
                    <strong
                    ><h6 class="plan-cost white-text">
                        ({{ this.userData.roles[0].name }})</h6>
                    </strong>
                </p>
            </div>
            <hr class="w-100"/>
        </div>
    </mdb-side-nav-2>
</template>
<script>

export default {
    name: "SideNavigationBar",
    data() {
        return {
            show: true,
            loaded: false,
            slimCollapsed: true,
            userData: {},
            navops: []
        };
    },
    watch: {
        '$root.private.userData.fetched': {
            handler: function () {
                let rt = this.$root.routes.filter(route => {
                    return 'sidenav' in route;
                });

                this.navops = []
                for (let i = 0; i < rt.length; i++) {
                    this.navops.push(rt[i].sidenav)
                }
                this.userData = this.$root.private.userData.data;
                this.loaded = true;
            },

        },
    },
    mounted() {
        this.$root.initUserData()
    },
};
</script>

<style scoped>
.navbar i {
    cursor: pointer;
    color: white;
}

.background-color {
    color: #9F9F9F;
}
</style>