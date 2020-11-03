<template>
    <div id="register" class="centered-block container-fluid form-elegant image ">
        <section class="form-elegant mt-5">
            <mdb-col md="5" class="mx-auto">
                <mdb-card class="greyBack">
                    <mdb-card-header class="text-center blue-gradient ">
                        <mdb-card-title tag="h4" bold class="white-text w-100 mt-1">Εγγραφή</mdb-card-title>
                    </mdb-card-header>
                    <mdb-card-body class="greyBack">
                        <form novalidate @submit="checkForm">
                            <div class="white-text">
                                <mdb-row>
                                    <mdb-col>
                                        <mdb-input v-model="formInfo.name"
                                                   icon="user"
                                                   label="Όνομα"
                                                   type="text"
                                                   required
                                                   class="mb-3"/>
                                    </mdb-col>
                                    <mdb-col>
                                        <mdb-input v-model="formInfo.surname"
                                                   label="Επίθετο"
                                                   type="text"
                                                   required
                                                   class="mb-3"/>
                                    </mdb-col>
                                </mdb-row>
                                <mdb-row>
                                    <mdb-col>
                                        <mdb-input v-model="formInfo.username"
                                                   icon="key"
                                                   label="Όνομα χρήστη"
                                                   group
                                                   type="text" required
                                                   class="mb-3"/>
                                    </mdb-col>
                                    <mdb-col>
                                        <mdb-input v-model="formInfo.password"
                                                   label="Κωδικός"
                                                   type="password"
                                                   required
                                                   class="mb-3"/>
                                    </mdb-col>
                                </mdb-row>
                                <mdb-row>
                                    <mdb-col>
                                        <mdb-input v-model="formInfo.email" class="mb-3" label="email" icon="envelope"
                                                   group type="email"
                                                   validate error="wrong"
                                                   required
                                                   success="right"/>
                                    </mdb-col>
                                </mdb-row>
                                <mdb-row>
                                    <mdb-col class="mb-2 mt-3 d-flex justify-content-center">
                                        <mdb-form-inline>
                                            <mdb-input required type="radio" id="option5-1"
                                                       name="groupOfMaterialRadios2" radioValue="user"
                                                       v-model="formInfo.role"
                                                       label="Χρήστης"/>
                                            <mdb-input required type="radio" id="option5-2"
                                                       name="groupOfMaterialRadios2" radioValue="owner"
                                                       v-model="formInfo.role"
                                                       label="Ιδιοκτήττης Cinema"/>
                                        </mdb-form-inline>
                                    </mdb-col>
                                </mdb-row>
                                 <mdb-row v-if="formInfo.role === 'owner'" >
                                    <mdb-col class="mb-2 mt-3 d-flex justify-content-center">
                                        <mdb-input v-model="formInfo.cinemaName"
                                                   label="Όνομα κινηματογράφου"
                                                   type="text"
                                                   required
                                                   icon="building"
                                                   class="mb-3"/>
                                    </mdb-col>
                                </mdb-row>
                            </div>
                            <mdb-row>
                                <mdb-col class=" d-flex justify-content-center">
                                    <mdb-btn @click="cancelReg" color="danger" rounded> Ακύρωση</mdb-btn>
                                </mdb-col>
                                <mdb-col class=" d-flex justify-content-center">
                                    <mdb-btn type="submit" @click="submitReg" color="grey" rounded> Υποβολή</mdb-btn>
                                </mdb-col>
                            </mdb-row>
                        </form>
                    </mdb-card-body>
                </mdb-card>
            </mdb-col>
        </section>
        <mdb-modal :show="shown" @close="closeSuccessModal" info>
            <mdb-modal-header>
                <mdb-modal-title>Επιβεβαίωση εγγραφής</mdb-modal-title>
            </mdb-modal-header>
            <mdb-modal-body>
                <mdb-icon icon="check" size="4x" class="mb-3 animated rotateIn"/>
                <p class="text-center">
                    Ευχαριστούμε για την εγγραφή σας. Αναμένετε επιβεβαίωση.
                </p>
            </mdb-modal-body>
        </mdb-modal>
    </div>
</template>

<script>

export default {
    name: "Register",
    data() {
        return {
            shown: false,
            formInfo: {}
        };
    },
    methods: {
        closeSuccessModal: function () {
            this.shown = false;
            this.$router.push('Login');
        },
        cancelReg: function () {
            this.$router.push('Login');
        },
        checkForm: function (event) {
            event.target.classList.add('was-validated');
            event.preventDefault();
        },
        submitReg: function () {
            const formData = new FormData();
            formData.append('formData', JSON.stringify(this.formInfo));
            if ('rat' in this.$route.query) {
                formData.append('Token', this.$route.query.rat);
            }
            formData.append('Type', 'Registration');
            this.$axios.post('http://localhost:8000/api/UserProfile/', formData, {headers: {'Content-Type': 'multipart/form-data'}})
                .then(() =>{
                    this.shown = true;
                })
                .catch(this.$notifyAction.error);
        }

    }
};
</script>

<style>
.md-form label {
    color: white !important;
}

.image {
    background-image: url('../../media/movieCollection.png');
    min-height: 100vh;
    min-width: 100vw;
}

.greyBack{
    background-color: dimgrey;
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








