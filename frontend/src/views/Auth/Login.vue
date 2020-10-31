<template>
    <div id="login" class="centered-block container-fluid form-elegant image">
        <section class="form-elegant mt-5">
            <mdb-col sm="3" md="3" lg="3" class="mx-auto">
                <mdb-card>
                    <mdb-card-body class="mx-4">
                        <form @submit.prevent="login">
                            <div class="text-center">
                                <h3 class="dark-grey-text mb-5"><strong>Είσοδος</strong></h3>
                            </div>
                            <mdb-input v-model="credentials.username" label="Username" type="text" required
                                       class="mb-5"/>
                            <mdb-input v-model="credentials.password" label="Password" type="password"
                                       containerClass="mb-0"/>
                            <div class="text-center mb-3">
                                <mdb-btn type="submit" gradient="blue" rounded class="btn-block z-depth-1a">Είσοδος
                                </mdb-btn>
                            </div>
                        </form>
                    </mdb-card-body>
                    <mdb-modal-footer class="mx-5 pt-3 mb-1">
                        <p class="font-small grey-text d-flex justify-content-end">Δεν είστε μέλος;
                            <router-link :to="{name: 'Register', query: {next: $route.query.next}}">Εγγραφή
                            </router-link>
                        </p>
                    </mdb-modal-footer>
                </mdb-card>
            </mdb-col>
        </section>
    </div>
</template>

<script>


export default {
    beforeCreate: function () {
        document.body.className = 'login';
    },
    name: 'Login',
    data() {
        return {
            credentials: {},
            valid: true,
            loading: false,
        };
    },
    methods: {
        login: function () {
            if (this.loading) return;
            this.loading = true;
            this.$axios.post('http://localhost:8000/api/auth/token/', this.credentials)
                .then(res => {
                    this.$session.start();
                    this.$session.set('access', res.data.access);
                    this.$session.set('refresh', res.data.refresh);
                    this.$root.initAxiosHeaders();
                    this.$root.authenticated = true;
                    this.loading = false;
                    this.$router.push({name: 'Home', query: this.$router.query});
                    this.$root.initUserData();
                })
                .catch(e => {
                    console.log(e);
                    this.loading = false;
                    this.$notify({
                        text: "Λάθος όνομα χρήστη ή κωδικού",
                        type: 'error'
                    });
                });
        },
        created() {
            if (this.$root.authenticated) {
                this.$router.push({name: 'Home', query: this.$router.query});
            }
        }
    }
}
</script>


<style>

.image {
    background-image: url('../../media/movieCollection.png');
    min-height: 100vh;
    min-width: 100vw;
}

.transparent {
    background-color: white !important;
    opacity: 0.65;
    border-color: transparent !important;
}

.form-elegant .font-small {
    font-size: 0.8rem;
}

.form-elegant .z-depth-1a {
    -webkit-box-shadow: 0 2px 5px 0 rgba(55, 161, 255, 0.26), 0 4px 12px 0 rgba(121, 155, 254, 0.25);
    box-shadow: 0 2px 5px 0 rgba(55, 161, 255, 0.26), 0 4px 12px 0 rgba(121, 155, 254, 0.25);
}

.form-elegant .z-depth-1-half,
.form-elegant .btn:hover {
    -webkit-box-shadow: 0 5px 11px 0 rgba(85, 182, 255, 0.28), 0 4px 15px 0 rgba(36, 133, 255, 0.15);
    box-shadow: 0 5px 11px 0 rgba(85, 182, 255, 0.28), 0 4px 15px 0 rgba(36, 133, 255, 0.15);
}
</style>