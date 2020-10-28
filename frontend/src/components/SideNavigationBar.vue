<template>
    <mdb-side-nav-2
        :value="true"
        :data="navigation"
        side
        slim
        expand-on-hover
        :slim-collapsed="slimCollapsed"
        @toggleSlim="slimCollapsed = $event"
        sidenav-class="blue accent-4"
        color="white"
    >
        <div slot="header">
            <div
                class="d-flex align-items-center my-4"
                :class="
          slimCollapsed
            ? 'justify-content-center'
            : 'justify-content-start'
        "
            >
                <mdb-avatar :width="40" style="flex: 0 0 auto">
                    <img
                        src="https://mdbootstrap.com/img/Photos/Avatars/avatar-2.jpg"
                        class="img-fluid rounded-circle z-depth-1"
                    />
                </mdb-avatar>
                <p
                    class="m-t mb-0 ml-4 p-0"
                    style="flex: 0 2 auto"
                    v-show="!slimCollapsed"
                >
                    <strong
                    >Ann Smith
                        <mdb-icon
                            color="success"
                            icon="circle"
                            class="ml-2"
                            size="sm"
                        />
                    </strong>
                </p>
            </div>
            <hr class="w-100"/>
            <mdb-nav-item @click="logout">
                <mdb-icon icon="sign-out-alt" class="mr-1"/>
            </mdb-nav-item>
        </div>
    </mdb-side-nav-2>
</template>
<script>
import {mdbSideNav2, mdbIcon, mdbAvatar} from "mdbvue";

export default {
    name: "SideNavigationBar",
    components: {
        mdbIcon,
        mdbAvatar,
        mdbSideNav2
    },
    methods: {
        logout: function () {
            this.$session.destroy();
            window.location.reload(true);
        },
    },
    data() {
        return {
            show: true,
            slimCollapsed: true,
            navigation: [
                {
                    name: "Home",
                    to: "/",
                    icon: "home"
                },
                {
                    name: "CSS",
                    to: "/css",
                    icon: "css3",
                    fab: true
                },
                {
                    name: "Components",
                    to: "/components",
                    icon: "cubes"
                },
                {
                    name: "Advanced",
                    to: "/advanced",
                    icon: "code"
                }
            ]
        };
    }
};
</script>

<style scoped>
.navbar i {
    cursor: pointer;
    color: white;
}
</style>