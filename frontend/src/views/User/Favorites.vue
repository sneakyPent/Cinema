<template>
    <div class="ml-5 mr-4">
        <mdb-container class="text-center">
            <div class="d-flex justify-content-center ml-5 rcorners">
                <Table
                    class="mt-5"
                    v-if="fetched"
                    :buttons="tableButtons"
                    :tableTitle="'Αγαπημένες Ταινίες'"
                    :tableIcon="'star'"
                    checkingRow
                    :tableData="tableData"
                    :availableCols="availableCols"
                    @rowClick="selectUserFromTable($event)"
                    @buttonsClick="tableButtonsHandler($event)"
                />
            </div>
        </mdb-container>
    </div>
</template>

<script>

import Table from '../../components/Structure/Table';
import {mdbContainer, Sticky} from 'mdbvue';

export default {
    name: "Favorites",
    directives: {
        sticky: Sticky
    },
    components: {
        Table,
        mdbContainer,
    },
    data: function () {
        return {
            availableCols: [],
            tableData: {
                data: []
            },
            fetched: false,
            buttonsChange: false,
            moviesList: [],
            modal: false,
            movieInfo: {},
            tableButtons: [
                {
                    label: 'Αφαίρεση απο τα αγαπημένα',
                    name: 'delete',
                    id: 1,
                    icon: 'times',
                    forceEnable: false
                },
            ],
        };
    },
    mounted: function () {
        this.getFavorites();
        this.getAvailableCols();
    },
    methods: {
        tableButtonsHandler: function (el) {
            const [button, rows] = el
            switch (button.name) {
                case 'delete':
                    this.removeMovie(rows);
                    break;
                default:
                    console.log('default');
            }
        },
        getAvailableCols: function () {
            this.$axios.get('/api/Movie/?fields')
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
        getFavorites: function () {
            const query = '/api/Favorite/';
            this.$axios.get(query)
                .then(
                    usres => {
                        this.moviesList = usres.data;
                        this.fixingTableData();
                    })
                .catch(this.$notifyAction.error);
        },
        addMovie: function () {
            this.movieModalChangesDisabled = false;
            this.modalTitle = 'Εισαγωγή νέας ταινίας'
            let movie = {
                title: '',
                category: '',
                startDate: '',
                endDate: ''
            }
            this.openModal(movie);
        },
        removeMovie: function (movies) {
            for (let i = 0; i < movies.length; i++) {
                this.$axios.delete('/api/Favorite/' + movies[i] + '/')
                    .then(() => {
                        this.getFavorites();
                        this.$notify({
                            text: 'Επιτυχής Διαγραφή!',
                            type: 'success'
                        });
                    })
                    .catch(this.$notifyAction.error);
            }
        },
        fixingTableData: function () {
            // fix the format for the table tableData prop
            const data = [];
            const headers = [];
            const val = this.availableCols;
            const mList = this.moviesList
            for (let i = 0; i < mList.length; i++) {
                const tmpdict = {};
                for (let j = 0; j < val.length; j++) {
                    tmpdict[val[j].value.toLowerCase()] = this.$tr(mList[i][val[j].value]);
                }
                data.push(tmpdict);
            }
            // headers.push({label: 'id', field: 'id', sorting: true, type: 'string', clickable: false});
            for (let i = 0; i < val.length; i++) {
                if (!(val[i].value.toLowerCase() === 'id') && !(val[i].value.toLowerCase() === 'availability'))
                    headers.push({
                        label: this.$tr(val[i].text.toString()),
                        field: val[i].value.toString().toLowerCase(),
                        sorting: true,
                        type: 'string',
                        clickable: false
                    });
            }
            this.tableData = {headers: headers, data: data};
        },
    },
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