<template>
    <mdb-side-nav-2
        :value="true"
        :data="navigation"
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
                        {{ this.userData.last_name + ' ' + this.userData.first_name }}</h6>
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
                        ({{ this.userData.role }})</h6>
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
    computed: {
        navigation: function () {
            let nv = [];
            let rt = this.$root.routes.filter(route => {
                return 'sidenav' in route;
            });
            for (let i = 0; i < rt.length; i++) {
                nv.push(rt[i].sidenav)
            }
            return nv;
        },
    },
    data() {
        return {
            show: true,
            slimCollapsed: true,
            userData: {}
        };
    },
    methods: {
        initData: function() {
            const accessToken = this.$session.get('access');
            const tokenData = this.$root.parseJwt(accessToken);
            this.$axios.get('http://localhost:8000/api/UserProfile/' + tokenData.user_id + '/')
                .then(res => {
                    this.userData = res.data;
                })
                .catch(this.$notifyAction.error);
        },
    },
    mounted: function() {
        this.initData()
    }
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