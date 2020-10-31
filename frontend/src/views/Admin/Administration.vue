<template>
    <div class="ml-5 mr-4">
        <mdb-container class="text-center">
            <hr>
        </mdb-container>
        <div class="d-flex justify-content-center ml-5">
            <Table
                v-if="fetched"
                :buttons="tableButtons"
                :tableTitle="'Χρήστες'"
                checkingRow
                doublebutton
                :tableData="tableData"
                :availableCols="availableCols"
                :doublebuttonchange="buttonsChange"
                @doubleButtonClick="doubleButtonHandler($event)"
                @oneRowCheck="lockUnlock($event)"
                @rowClick="selectUserFromTable($event)"
                @buttonsClick="tableButtonsHandler($event)"
            />
        </div>
        <user-profile-modal v-if="modal" :closing="closeModal" :userInfo="userInfo" state="Approved" :submit="submit"
                            :decline="decline"/>
    </div>
</template>

<script>
import UserProfileModal from '../../components/Structure/UserProfileModal';
import Table from '../../components/Structure/Table';
import {mdbContainer, Sticky} from 'mdbvue';

export default {
    name: 'Users',
    directives: {
        sticky: Sticky
    },
    components: {
        Table,
        UserProfileModal,
        mdbContainer,
    },
    data: function () {
        return {
            // pageLimit: 25,
            // pageOffset: 0,
            // dataLength: 0,
            // orderby: 'name',
            // search: '',
            // lastQuery: '',
            selectedUser: '',
            availableCols: [],
            tableData: {
                data: []
            },
            fetched: false,
            buttonsChange: false,
            usersList: [],
            modal: false,
            userInfo: {
                surname: '',
                name: '',
                username: '',
                email: '',
                role: '',
                is_active: false

            },
            tableButtons: [
                {
                    label: 'Διαγραφή',
                    name: 'delete',
                    id: 1,
                    icon: 'times',
                    forceEnable: false
                },
            ],

            testing: {
                headers: [
                    {
                        label: 'ID',
                        field: 'id',
                        sorting: true,
                        type: 'string',
                        clickable: false

                    },
                    {
                        label: 'Name',
                        field: 'name',
                        sorting: true,
                        type: 'string',
                        clickable: false
                    },
                    {
                        label: 'Position',
                        field: 'position',
                        sorting: true,
                        type: 'string',
                        clickable: false
                    },
                    {
                        label: 'Office',
                        field: 'office',
                        sorting: false,
                        type: 'string',
                        clickable: false
                    },
                    {
                        label: 'Age',
                        field: 'age',
                        sorting: true,
                        type: 'string',
                        clickable: false
                    },
                    {
                        label: 'Start date',
                        field: 'date',
                        sorting: true,
                        type: 'string',
                        clickable: false
                    },
                    {
                        label: 'Salary',
                        field: 'salary',
                        sorting: true,
                        type: 'string',
                        clickable: false
                    }
                ],
                data: [
                    {
                        id: '1',
                        name: 'Tiger Nixon',
                        position: 'System Architect',
                        office: 'Edinburgh',
                        age: '61',
                        date: '2011/04/25',
                        salary: '$320'
                    },
                    {
                        id: '2',
                        name: 'Garrett Winters',
                        position: 'Accountant',
                        office: 'Tokyo',
                        age: '63',
                        date: '2011/07/25',
                        salary: '$170'
                    },

                ]
            },
        };
    },
    mounted: function () {
        this.getAllUser();
        this.getAvailableCols();
    },
    methods: {
        selectUserFromTable: function (user) {
            this.selectedUser = Number.parseInt(user);
        },
        tableButtonsHandler: function (button) {
            switch (button.name) {
                case 'delete':
                    console.log('delete');
                    break;
                case 'add':
                    this.collabModal = true;
                    break;
                default:
                    console.log('default');
            }
        },
        getAvailableCols: function () {
            this.$axios.get('http://localhost:8000/api/UserProfile/?fields')
                .then(res => {
                    for (let i = 0; i < res.data.fields.length; i++) {
                        this.availableCols.push({
                            selected: false,
                            value: res.data.fields[i],
                            text: res.data.fields[i]
                        });

                    }
                    this.fixingTableData();
                    this.fetched = true;
                })
                .catch(this.$notifyAction.error);
        },
        getAllUser: function () {
            const query = 'http://localhost:8000/api/UserProfile/?nonadmin';
            if (this.lastQuery === query) {
                return;
            }
            this.$axios.get(query)
                .then(
                    usres => {
                        console.log(usres);
                        this.lastQuery = query;
                        this.usersList = usres.data;
                        this.fixingTableData();
                    })
                .catch(this.$notifyAction.error);
        },
        openModal: function (user) {
            this.fillForm(user);
            this.modal = true;
        },
        closeModal: function () {
            this.modal = false;
            this.selectedUser = '';
        },
        submit: function () {
            this.$axios.post('/api/collaboration/update/', this.form)
                // eslint-disable-next-line no-unused-vars
                .then(res => {
                    this.getAllUser();
                    this.closeModal();
                    this.$notify({
                        text: this.$t('Changes applied!'),
                        type: 'success'
                    });
                })
                .catch(this.$notifyAction.error);
        },
        decline: function () {
            this.closeModal();
            this.$notify({
                text: this.$t('Changes dismissed!'),
                type: 'success'
            });
        },

        fillForm: function (user) {
            this.userInfo.surname = user.last_name;
            this.userInfo.name = user.first_name;
            this.userInfo.username = user.username;
            this.userInfo.email = user.email;
            this.userInfo.role = user.role;
            this.userInfo.is_active = user.is_active;

        },
        fixingTableData: function () {
            // fix the format for the table tableData prop
            const data = [];
            const headers = [];
            const val = this.availableCols;
            const uList = this.usersList.filter(el => {
                return el.UserProfile !== null;
            });
            for (let i = 0; i < uList.length; i++) {
                const tmpdict = {};
                for (let j = 0; j < val.length; j++) {
                    tmpdict[val[j].value.toLowerCase()] = uList[i][val[j].value.toLowerCase()];
                }
                data.push(tmpdict);
            }
            // headers.push({label: 'id', field: 'id', sorting: true, type: 'string', clickable: false});
            for (let i = 0; i < val.length; i++) {
                headers.push({
                    label: val[i].text.toString(),
                    field: val[i].value.toString().toLowerCase(),
                    sorting: true,
                    type: 'string',
                    clickable: false
                });
            }
            this.tableData = {headers: headers, data: data};
        },
        // setPage: function (itemsPerPage, offset, ordering, search) {
        //     this.pageLimit = itemsPerPage;
        //     this.pageOffset = offset;
        //     this.search = search;
        //
        //     if (ordering.charAt(0) === '-') {
        //         this.orderby = '-' + this.orderbyTranslation[ordering.split('-')[1]];
        //     } else {
        //         this.orderby = this.orderbyTranslation[ordering];
        //     }
        //     this.getAllUser();
        // }
    },
    watch: {
        selectedUser: function () {
            if (this.selectedUser !== '') {
                this.openModal(this.usersList.find(el => {
                    if (el.id !== null)
                        return el.id === this.selectedUser;
                }));
            }
        }
    }
}
;
</script>

<style scoped>

.form-control {
    color: black !important;
}

</style>