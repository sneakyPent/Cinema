<template>
    <mdb-modal id="movieModal" @close="closing" size="mx-auto" class="modal">
        <mdb-modal-header class="w-100 align-items-center">
            <mdb-modal-title class="w-100 align-items-center">
                <mdb-row class="justify-content-center ml-3">
                    {{ modalTitle}}
                </mdb-row>
                <!--				<mdb-badge class="float-right" :color="state === 'Pending' ? 'warning' : state === 'Approved' ? 'success' : 'danger'">{{ $t(state) }}</mdb-badge>-->
            </mdb-modal-title>
        </mdb-modal-header>
        <mdb-modal-body class="black-text">
            <form novalidate class="label">
                <div class="black-text" id="form_rows">
                    <mdb-row>
                        <mdb-col>
                            <mdb-input v-model="movieInfo.title" icon="film" label="Τίτλος" type="text"
                                       required :disabled=disableChanges
                                       invalidFeedback="Please provide a valid city." class="mb-3 "/>
                        </mdb-col>
                    </mdb-row>
                    <mdb-row>
                        <mdb-col>
                            <mdb-input v-model="movieInfo.category" icon="filter" label="Κατηγορία" type="text"
                                       required :disabled=disableChanges
                                       class="mb-3"/>
                        </mdb-col>
                    </mdb-row>
<!--                    <mdb-row>-->
<!--                        <mdb-col>-->
<!--                            <mdb-input v-model="movieInfo.cinema" icon="building" label="Κινηματογράφος" type="text"-->
<!--                                       required :disabled=true-->
<!--                                       class="mb-3"/>-->
<!--                        </mdb-col>-->
<!--                    </mdb-row>-->
                    <mdb-row>
                        <mdb-date-picker
                            class="ml-3"
                            :label="'Ημερομηνία Έναρξης'"
                            v-model="movieInfo.startDate"
                            required
                            autoHide
                            disabledPast
                            :option="$datepickerOptions()"
                            far icon="calendar-alt"
                        />
                    </mdb-row>
                    <mdb-row>
                        <mdb-date-picker
                            class="ml-3"
                            :label="'Ημερομηνία Λήξης'"
                            v-model="movieInfo.endDate"
                            required
                            autoHide
                            disabledPast
                            :option="$datepickerOptions()"
                            far icon="calendar-alt"
                        />
                    </mdb-row>
                </div>
                <mdb-row>
                    <mdb-col class=" d-flex justify-content-center">
                        <mdb-btn @click="decline" color="danger" rounded> Ακύρωση</mdb-btn>
                    </mdb-col>
                    <mdb-col class=" d-flex justify-content-center">
                        <mdb-btn @click="submit" color="grey" rounded> Υποβολή</mdb-btn>
                    </mdb-col>
                </mdb-row>
            </form>
        </mdb-modal-body>
    </mdb-modal>
</template>

<script>

export default {
    name: 'MovieModal',
    props: {
        movieInfo: {},
        modalTitle: String,
        disableChanges: Boolean,
        chose: String,
        closing: Function,
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
    color: black !important;
}

#form_rows .row .col .form-control {
    color: black !important;
}

#movieModal .modal-content {
    border-radius: 25px !important;
}

.mdb-vue-date .datepickbox .form-control {
    color: black !important;
   }

</style>

<style scoped>

</style>
