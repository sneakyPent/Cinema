<template>
    <div class="ml-5 mr-4">
        <mdb-container class="text-center">
            <div class="d-flex justify-content-center ml-5 rcorners">
                <Table
                    class="mt-5"
                    v-if="fetched"
                    :buttons="tableButtons"
                    :tableTitle="'Χρήστες'"
                    :tableIcon="'users'"
                    checkingRow
                    :tableData="tableData"
                    :availableCols="availableCols"
                    clickRow
                    @rowClick="selectUserFromTable($event)"
                    @buttonsClick="tableButtonsHandler($event)"
                />
            </div>
            <user-profile-modal v-if="modal" :closing="closeModal" :userInfo="userInfo" state="Approved"
                                @submitForm="submit($event[0])"
                                :decline="decline"/>
        </mdb-container>
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
            this.$axios.get('/api/Request/?fields')
                .then(res => {
                    for (let i = 0; i < res.data.fields.length; i++) {
                        this.availableCols.push({
                            selected: false,
                            value: res.data.fields[i],
                            text: this.$tr(res.data.fields[i])
                        });

                    }
                    this.fixingTableData();
                    this.fetched = true;
                })
                .catch(this.$notifyAction.error);
        },
        getAllUser: function () {
            const query = '/api/Request/';
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
                this.$axios.delete('/api/Request/' + users[i] + '/')
                    .then(() => {
                        this.getAllUser();
                        this.$notifyAction.success('Επιτυχής διαγραφή χρήστη!');
                    })
                    .catch(this.$notifyAction.error);
            }
        },
        submit: function (uInfo) {
			this.userInfo.surname=uInfo.surname
			this.userInfo.name=uInfo.name
			this.userInfo.username=uInfo.username
			this.userInfo.email=uInfo.email
			this.userInfo.role=uInfo.role
			this.userInfo.is_active=uInfo.is_active
			this.userInfo.cinema=uInfo.cinema
			const formData = new FormData();
            formData.append('formData', JSON.stringify(uInfo));
            if ('rat' in this.$route.query) {
                formData.append('Token', this.$route.query.rat);
            }
            formData.append('Type', 'update');
            const query = '/api/Request/' + this.userInfo.id + '/';
            this.$axios.put(query, formData, {headers: {'Content-Type': 'multipart/form-data'}})
                .then(() => {
                    this.$notifyAction.success('Επιτυχής αλλαγή στοιχείων χρήστη!');
                    this.getAllUser();
                    this.closeModal();

                })
                .catch(() => {
						this.$notifyAction.warning('Ανεπιτυχής αλλαγή δεδομένων χρήστη!');
						this.getAllUser();
						this.closeModal();
					}
				);
        },
        decline: function () {
            this.closeModal();
            this.$notifyAction.success('Απόρριψη αλλαγών');
        },
        fillForm: function (user) {
            this.userInfo.id = user.id;
            this.userInfo.name = user.userName;
            this.userInfo.email = user.email;
            this.userInfo.role = user.role;
            this.userInfo.is_active = user.is_active;
            this.userInfo.cinema = user.cinema;
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
                    tmpdict[val[j].value] = this.$tr(uList[i][val[j].value]);
                }
                data.push(tmpdict);
            }
            for (let i = 0; i < val.length; i++) {
                if (!(val[i].value.toLowerCase() === 'id'))
                    headers.push({
                        label: this.$tr(val[i].text.toString()),
                        field: val[i].value,
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