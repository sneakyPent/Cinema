<template>
    <mdb-modal @close="closing" size="lg">
        <mdb-modal-header>
            <mdb-modal-title class="w-100">
                <span>{{ userInfo.surname + " " + userInfo.name }}</span>
                <!--				<mdb-badge class="float-right" :color="state === 'Pending' ? 'warning' : state === 'Approved' ? 'success' : 'danger'">{{ $t(state) }}</mdb-badge>-->
            </mdb-modal-title>
        </mdb-modal-header>
        <mdb-modal-body>
            <!--			stepper for receivers of collaborations-->
            <mdb-stepper buttons :steps="1" @submit="submit" :options="stepperOptions">
                <template #1>
                    <h3 class="font-weight-bold pl-0 my-4 black-text">
                        <strong>Πληροφορίες Χρήστη</strong>
                    </h3>
                    <mdb-row>
                        <mdb-col md="12" lg="6">
                            <mdb-row>
                                <mdb-col>
                                    <mdb-input v-model="userInfo.name" icon="user" label="Όνομα" type="text"
                                               disabled class="mb-3 black-text"/>
                                </mdb-col>
                                <mdb-col>
                                    <mdb-input v-model="userInfo.surname" label="Επίθετο" type="text" disabled
                                               class="mb-3"/>
                                </mdb-col>
                            </mdb-row>
                            <mdb-row>
                                <mdb-col>
                                    <mdb-input v-model="userInfo.username" icon="key" label="Όνομα χρήστη" group
                                               type="text" disabled
                                               class="mb-3"/>
                                </mdb-col>
<!--                                <mdb-col>-->
<!--                                    <mdb-input v-model="userInfo.password" label="Κωδικός" type="text" disabled-->
<!--                                               class="mb-3"/>-->
<!--                                </mdb-col>-->
                            </mdb-row>
                            <mdb-row>
                                <mdb-col>
                                    <mdb-input v-model="userInfo.email" class="mb-3" label="email" icon="envelope"
                                               group type="email"
                                               validate error="wrong" disabled
                                               success="right"/>
                                </mdb-col>
                            </mdb-row>
                            <mdb-row>
                                <mdb-col class="mb-2 mt-3 d-flex justify-content-left">
                                    <mdb-form-inline>
                                        <mdb-input required type="radio" id="role-1"
                                                   name="groupOfMaterialRadios2" radioValue="user"
                                                   v-model="userInfo.role"
                                                   label="Χρήστης"/>
                                        <mdb-input required type="radio" id="role-2"
                                                   name="groupOfMaterialRadios2" radioValue="owner"
                                                   v-model="userInfo.role"
                                                   label="Ιδιοκτήττης Cinema"/>
                                    </mdb-form-inline>
                                </mdb-col>
                            </mdb-row>
                            <mdb-row>
                                <mdb-col class="mb-2 mt-3 d-flex justify-content-left">
                                    <mdb-form-inline>
                                        <mdb-input required type="radio" id="active"
                                                   name="groupOfMaterialRadios1" radioValue="True"
                                                   v-model="userInfo.is_active"
                                                   label="Ενεργός"/>
                                        <mdb-input required type="radio" id="non-active"
                                                   name="groupOfMaterialRadios1" radioValue="False"
                                                   v-model="userInfo.is_active"
                                                   label="Ανενεργός"/>
                                    </mdb-form-inline>
                                </mdb-col>
                            </mdb-row>
                        </mdb-col>
                    </mdb-row>
                </template>
            </mdb-stepper>
        </mdb-modal-body>
    </mdb-modal>
</template>

<script>
/**
 UserProfileModal
 give for props
 -submit function
 -decline function
 -the userinfo in dictionary
 {
		    tradeName
		    surname
		    name
		    fullName
		    username
		    email
		    mobile
		    phone
		    fullAddress
		    tin
		    chamberRegistryNumber
		    professionStartDate
		    licenseExpirationDate
		    message
		    files

		 }
 -the userCred in dictionary
 {
	        role
		    subscriptionExpirationDate
		    partnersNumberLimit
		    features
		    companies
	    }

 if preselected value are desired set selected:true in the given objects wanted to be selected

 */
//

export default {
    name: 'UserProfileModal',
    props: {
        userInfo: {},
        chose: String,
        closing: Function,
        state: String,
        submit: Function,
        decline: Function,
    },
    data: function () {
        return {
            dateChange: false,
            stepperOptions: {
                submitBtn: {
                    text: 'Υποβολή',
                },
            },
        };
    },
}
;
</script>

<style scoped>
.form-control {
    color: black;
}
</style>
