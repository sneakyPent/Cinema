<template>
    <mdb-modal @close="closing" size="mx-auto" class="modal">
        <mdb-modal-header class="w-100 align-items-center">
            <mdb-modal-title class="w-100 align-items-center">
                <mdb-row class="justify-content-center ml-3">
                    {{ userInfo.surname + " " + userInfo.name }}
                </mdb-row>
                <!--				<mdb-badge class="float-right" :color="state === 'Pending' ? 'warning' : state === 'Approved' ? 'success' : 'danger'">{{ $t(state) }}</mdb-badge>-->
            </mdb-modal-title>
        </mdb-modal-header>
        <mdb-modal-body class="black-text">
            <form novalidate class="label">
                <div class="black-text">
                    <mdb-row>
                        <mdb-col>
                            <mdb-input v-model="userInfo.name" icon="user" label="Όνομα" type="text"
                                       required disabled
                                       invalidFeedback="Please provide a valid city." class="mb-3 "/>
                        </mdb-col>
                    </mdb-row>
                    <mdb-row>
                        <mdb-col>
                            <mdb-input v-model="userInfo.surname" icon="user" label="Επίθετο" type="text"
                                       required disabled
                                       class="mb-3"/>
                        </mdb-col>
                    </mdb-row>
                    <mdb-row>
                        <mdb-col>
                            <mdb-input v-model="userInfo.username" icon="key" label="Όνομα χρήστη" group
                                       type="text" required disabled
                                       class="mb-3"/>
                        </mdb-col>
                    </mdb-row>
                    <mdb-row>
                        <mdb-col>
                            <mdb-input v-model="userInfo.email" class="mb-3" label="email" icon="envelope"
                                       group type="email"
                                       validate error="wrong"
                                       required
                                       disabled
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
                </div>
                <mdb-row>
                    <mdb-col class=" d-flex justify-content-center">
                        <mdb-btn @click="decline" color="danger" rounded> Ακύρωση</mdb-btn>
                    </mdb-col>
                    <mdb-col class=" d-flex justify-content-center">
                        <mdb-btn type="submit" @click="submit" color="grey" rounded> Υποβολή</mdb-btn>
                    </mdb-col>
                </mdb-row>
            </form>
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

<style>
.md-form label {
    color: grey !important;
}

.modal-content {
    border-radius: 25px !important;
}


</style>

<style scoped>

</style>
