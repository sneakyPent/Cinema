<template>
    <div id="login" class="centered-block container-fluid form-elegant image">
        <section class="form-elegant mt-5">
            <mdb-col sm="3" md="3" lg="3" class="mx-auto">
                <mdb-card>
                    <mdb-card-header class="text-center blue-gradient ">
                        <mdb-card-title tag="h4" bold class="white-text w-100 mt-1">Είσοδος</mdb-card-title>
                    </mdb-card-header>
                    <mdb-card-body class="greyBack">
                        <form @submit.prevent="login"
                                       >
                            <mdb-input v-model="credentials.username"
                                       label="Όνομα χρήστη"
                                       type="text"
                                       required
                                       class="mb-5 white-text"
                            />
                            <mdb-input v-model="credentials.password"
                                       label="Κωδικός"
                                       :type="passwordType"
                                       required
                                       containerClass="mb-5 white-text"
                            >
                                <i class="fas" :class="[passwordIcon]" @click="hidePassword = !hidePassword"></i>
                            </mdb-input>
                            <div class="text-center mb-3">
                                <mdb-btn type="submit" gradient="blue" rounded class="btn-block z-depth-1a">Είσοδος
                                </mdb-btn>
                            </div>
                        </form>
                    </mdb-card-body>
                    <mdb-modal-footer class="greyBack">
                        <p class="font-small grey-text d-flex justify-content-end white-text">Δεν είστε μέλος;
                            <router-link class=" cyan-text" :to="{name: 'Register', query: {next: $route.query.next}}">
                                Εγγραφή
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
            credentials: {
                'grant_type': 'password',
            },
            valid: true,
            loading: false,
            hidePassword: true
        };
    },
    methods: {
        login: function () {
            if (this.loading) return;
            this.loading = true;
            let qs = require('qs');
            let headers= {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic ' + btoa(this.$getClient_id()+ ':' + this.$getClient_secret())
            }
            this.$axios.post('/oauth2/token', qs.stringify(this.credentials) , {headers: headers})
                .then(res => {
                    this.$session.set('access', res.data.access_token);
                    this.$session.set('refresh', res.data.refresh_token);
                    this.$root.initAxiosHeaders(this.credentials);
                    this.$root.authenticated = true;
                    this.loading = false
                    this.$router.push({name: 'Home', query: this.$router.query});
                })
                .catch(e => {
                    console.log(e)
                    this.loading = false;
                    this.$notify({
                        text: "Λάθος όνομα χρήστη ή κωδικού",
                        type: 'error'
                    });
                })
        },
        created() {
            if (this.$root.authenticated) {
                this.$router.push({name: 'Home', query: this.$router.query});
            }
        }
    },
    computed: {
        passwordType() {
            return this.hidePassword ? 'password' : 'text'
        },
        passwordIcon() {
            return this.hidePassword ? 'fa-eye' : 'fa-eye-slash'
        }
    }
}
</script>


<style>

.form-control {
    color: white !important;
}

.greyBack {
    background-color: dimgrey;
}

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