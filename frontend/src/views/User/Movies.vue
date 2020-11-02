<template>
    <div class="ml-5 mr-4">
        <mdb-container class="text-center">
            <div class="d-flex justify-content-center ml-5 rcorners">
                <Table
                    class="mt-5"
                    v-if="fetched"
                    :tableTitle="'Τανίες'"
                    :tableIcon="'film'"
                    :tableData="tableDat"
                    :filters="filters"
                    :rowButtons="tableRowButtons"
                    @favs="addToFavorite($event)"
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
    name: "Movies",
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
            headers: [],
            filters: [
                {
                    id:1,
                    name: 'Τίτλος',
                    placeholder: 'Τίτλος',
                    value: ''
                },
                {
                    id:2,
                    name: 'Κινηματογράφος',
                    placeholder: 'Κινηματογράφος',
                    value: ''
                },
                {
                    id:3,
                    name: 'Κατηγορία',
                    placeholder: 'Κατηγορία',
                    value: ''
                },
                {
                    id:4,
                    name: 'Ημερομηνία Προβολής',
                    placeholder: 'Ημ. Προβολής',
                    value: ''
                },

            ],
            tableRowButtons: {
                nonFavorite: {
                    group: 'favs',
                    class: "far fa-star fa-lg",
                },
                favorite: {
                    group: 'favs',
                    class: "fas fa-star fa-lg favorite_star",
                },
            },
            fetched: false,
            buttonsChange: false,
            favoriteMovies: [],
            moviesList: [],
            favoriteList: [],
            modal: false,
            movieInfo: {},
        };
    },
    mounted: function () {
        this.updateLists();
        this.getAvailableCols();
        this.getMovies();

    },
    methods: {
        updateLists: function () {
            this.getFavorites();
            this.getMix()
        },
        addToFavorite: function (el) {
            let mv = this.moviesList.filter(mv => {
                return mv.id === el[0]
            }).pop()
            if (this.favoriteList.title.indexOf(mv.title) > -1)
                this.deleteFromFavorites(mv)
            else
                this.addFavorite(el[0])
        },
        deleteFromFavorites: function (movie) {
            let delMovie = this.favoriteMovies.filter(mv => {
                return mv.title === movie.title
            }).pop()
            this.$axios.delete('http://localhost:8000/api/Favorite/' + delMovie.id + '/')
                .then(() => {
                    this.$notifyAction.success('Η ταινία διεγράφει απο τα αγαπημένα επιτυχώς!');
                    this.updateLists();
                })
                .catch(this.$notifyAction.error);
        },
        addFavorite: function (movies) {
            const query = 'http://localhost:8000/api/Favorite/';
            this.$axios.post(query, {id: movies})
                .then(() => {
                    this.$notifyAction.success('Η ταινία σας προστέθηκε στα αγαπημένα επιτυχώς!');
                    this.fetched = true;
                    this.updateLists();
                })
                .catch(() => {
                        this.$notifyAction.warning('Η ταινία σας υπάρχει ήδη στα αγαπημένα!')
                    }
                );

        },
        getAvailableCols: function () {
            this.$axios.get('http://localhost:8000/api/Movie/?fields')
                .then(res => {
                    for (let i = 0; i < res.data.fields.length; i++) {
                        this.availableCols.push({
                            selected: false,
                            value: res.data.fields[i],
                            text: res.data.fields[i]
                        });

                    }
                    this.createTableHeaders();
                    this.fetched = true;
                })
                .catch(this.$notifyAction.error);
        },
        getFavorites: function () {
            const query = 'http://localhost:8000/api/Favorite/';
            this.$axios.get(query)
                .then((res) => {
                    this.favoriteMovies = res.data
                })
                .catch((response) => {
                        this.$notifyAction.error(response)
                    }
                );
        },
        getMovies: function () {
            const query = 'http://localhost:8000/api/Movie';
            this.$axios.get(query)
                .then(
                    usres => {
                        this.moviesList = usres.data;
                    })
                .catch(this.$notifyAction.error);
        },
        getMix: function () {
            const query = 'http://localhost:8000/api/Favorite/?titleList';
            this.$axios.get(query)
                .then((res) => {
                    this.favoriteList = res.data
                })
                .catch((response) => {
                        this.$notifyAction.error(response)
                    }
                );
        },
        createTableHeaders: function () {
            const headers = [];
            const val = this.availableCols;
            // Add the row buttons to the headers
            let butList = this.tableRowButtons;
            for (let but in butList) {
                if ((headers.length === 0) || !(headers.filter(header => header.field === butList[but].group).length > 0))
                    headers.push({
                        label: '',
                        field: butList[but].group,
                        sorting: false,
                        type: 'btn',
                        clickable: true,
                    });
            }
            // Get the headers from the table data fields
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
            this.headers = headers;
        },

    },
    computed: {
        tableDat: function () {
            const tData = {};
            const data = [];
            const val = this.availableCols;
            const mList = this.moviesList
            for (let i = 0; i < mList.length; i++) {
                const tmpdict = {};
                for (let j = 0; j < val.length; j++) {
                    tmpdict[val[j].value.toLowerCase()] = mList[i][val[j].value];
                }
                if (this.favoriteList.title.indexOf(mList[i].title) > -1)
                    tmpdict.type = 'favorite';
                else
                    tmpdict.type = 'nonFavorite'

                data.push(tmpdict);
            }

            tData.data = data
            tData.headers = this.headers;
            return tData;
        }
    }
};
</script>

<style>
.favorite_star {
    color: orange !important;
}

.form-control {
    color: black !important;
}

.rcorners {
    border-radius: 25px;
}

</style>