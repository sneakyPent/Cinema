<template>
    <div class="ml-5 mr-4">
        <mdb-container class="text-center">
            <hr>
        </mdb-container>
        <div class="d-flex justify-content-center ml-5 rcorners">
            <Table
                v-if="fetched"
                :buttons="tableButtons"
                :tableTitle="'Χρήστες'"
                :tableIcon="'users'"
                checkingRow
                :tableData="tableData"
                :availableCols="availableCols"
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
        tableButtonsHandler: function (el) {
            const [button, rows] = el
            switch (button.name) {
                case 'delete':
                    this.deleteUsers(rows);
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
            this.$axios.get(query)
                .then(
                    usres => {
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
        deleteUsers: function (users) {
            for (let i = 0; i < users.length; i++) {
                this.$axios.delete('http://localhost:8000/api/UserProfile/' + users[i] + '/')
                .then( () => {
                    this.getAllUser();
                    this.$notifyAction.success('Επιτυχής διαγραφή χρήστη!');
                })
                .catch(this.$notifyAction.error);
            }
        },
        submit: function () {
            const query = 'http://localhost:8000/api/UserProfile/' + this.userInfo.id + '/' ;
            this.$axios.put(query, this.userInfo)
                .then(() => {
                    this.$notifyAction.success('Επιτυχής αλλαγή στοιχείων χρήστη!');
                    this.getAllUser();
                    this.closeModal();

                })
                .catch(this.$notifyAction.error);
        },
        decline: function () {
            this.closeModal();
            this.$notifyAction.success('Απόρριψη αλλαγών');
        },

        fillForm: function (user) {
            this.userInfo.id = user.id;
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
                if (!(val[i].value.toLowerCase() === 'id'))
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
.rcorners {
    border-radius: 25px;
}

</style>