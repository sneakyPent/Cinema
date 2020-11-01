<template>
    <div class="my-0 mp-0 d-md-inline-flex card p-3 pt-4 card-cascade narrower">
        <!--Card image-->
        <mdb-card
            class="
            gradient-card-header blue-gradient justify-content-around align-items-center text-light d-flex narrower display_flex
             view view-cascade my-1 overflow py-2 mx-3 mb-3 flex-column" style=" width: 1000px" >
            <mdb-row class="mt-1">
                <mdb-col>
                    <div class="flex_entry order-1 order-md-2 flex-grow-1">
                        <mdb-card-title tag="h4" bold class="white-text w-100 mt-1" >
                            <mdb-icon class="mx-2" :icon=tableIcon />
                            <span><strong style="font-family:Comic Sans MS;" >{{ tableTitle }}</strong></span>
                        </mdb-card-title>
                    </div>
                </mdb-col>
            </mdb-row>
            <mdb-row class="justify-content-between" style=" width: 800px">
                <mdb-col col="4">
                    <div class=" flex_entry d-flex justify-content-around order-3 order-md-1 flex-grow-1 mt-4 ">
                        <button
                            v-for="btn in singleButtons"
                            :disabled="multipleSelectedRows.length === 0 && !btn.forceEnable"
                            :key="btn.id"
                            :id="btn.id"
                            type="button"
                            @click="$emit('buttonsClick',[ btn, multipleSelectedRows])"
                            class="btn btn-outline-white btn-rounded btn-md px-2">
                            <span>{{ btn.label }}</span>
                            <mdb-icon class="fas mx-1" :icon="btn.icon"/>
                        </button>
                        <div v-if="doublebutton">
                            <dblButton
                                v-for="btn in doubleButtons"
                                :button="btn"
                                :key="btn.id"
                                :disabled="multipleSelectedRows.length !== 1 && !btn.forceEnable"
                                :primaryToSecondary="doublebuttonchange"
                                @click="doubleButtonClick($event)"/>
                        </div>
                    </div>
                </mdb-col >
                <mdb-col col="4" >
                    <div
                        class="flex_entry testing d-flex justify-content-around flex-wrap order-2 order-md-3 flex-grow-1 mb-0">
                        <mdb-select
                            caretStyle="color: white;"
                            style="white-space: nowrap;color: white;"
                            iconClass="d-flex justify-content-end"
                            color="primary"
                            multiple
                            selectAll
                            :visibleOptions="6"
                            :selectAllPlaceholder="'Επιλογή όλων'"
                            @getValue="getSelectFields"
                            :options="availableCols"
                            :label="'Πεδία'"
                        />
                    </div>
                </mdb-col>
            </mdb-row>
        </mdb-card>
        <!--/Card image-->
        <div class="mx-2 mx-md-3">
            <div class="d-flex justify-content-center">
                <div class="scrolling" style="display: inline">
                    <table class="table table-hover tableStyle ovfno table-bordered mx-auto " style="width: 1000px">
                        <thead>
                        <th :id="header.field" style="white-space: nowrap;"
                            v-for="header in headers" :key="header.field" scope="col">
                            <mdb-icon class='unclickable' mx-1 v-if="customizeColumns" icon="arrows-alt"/>
                            <span class='unclickable'> <strong> {{ header.label }}</strong> </span>
                            <!--								<mdb-icon class="right unclickable" v-if="header.sorting" icon="sort"/>-->
                        </th>

                        </thead>
                        <tbody>
                        <tr
                            style="white-space: nowrap;"
                            v-on:click="getSelectedRow($event)"
                            v-for="item in tableData.data"
                            :key="item.id"
                            :id="item.id"
                        >
                            <td v-bind:class="{ 'unclickable': true, 'checkboxCentering': header.type === 'checkbox'}"
                                v-for="header in headers"
                                :key="header.field"
                            >
                                <span class='unclickable' v-if="header.type === 'string'"> {{
                                        item[header.field]
                                    }}</span>
                                <mdb-input
                                    class="center"
                                    v-if="header.type === 'checkbox'"
                                    type="checkbox"
                                    :id="'c'+item.id"
                                    name="check"
                                    @change="getMultipleSelectedRows({selected: $event, id: item.id})"
                                />
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <!--			&lt;!&ndash;		                	PAGINATION                   &ndash;&gt;-->
            <!--			<div class=" my-2 my-md-2 w-100 pt-3 d-flex justify-content-end">-->
            <!--				<Pagination ref="pagination" :items="tableDataLength" @pagination="setPage"/>-->
            <!--			</div>-->
        </div>
    </div>
</template>

<script>``
import dblButton from '../../components/Inputs/doubleButton';

export default {
    props: {
        tableTitle: String,
        tableIcon: String,
        tableData: {},
        availableCols: Array,
        checkingRow: Boolean,
        buttons: Array,
        doublebutton: Boolean,
        doublebuttonchange: Boolean
    },
    components: {
        dblButton,
    },
    data: function () {
        return {
            customizeColumns: false,
            tableColumns: [],
            headers: [],
            selectedRow: -1,
            multipleSelectedRows: [],
            currentSort: 'id',
            currentSortDir: 'desc',
            orderby: '',
            search: ''
        };
    },
    mounted: function () {
        this.headers = this.tableData.headers;
        this.addCheckboxes();

    },
    methods: {
        doubleButtonClick: function (ev) {
            this.$emit('doubleButtonClick', ev);
        },
        getMultipleSelectedRows: function (newRow) {
            if (newRow.selected && !this.multipleSelectedRows.includes(newRow.id)) {
                this.multipleSelectedRows.push(newRow.id);
            } else if (!newRow.selected && this.multipleSelectedRows.includes(newRow.id)) {
                const rowindex = this.multipleSelectedRows.indexOf(newRow.id);
                this.multipleSelectedRows.splice(rowindex, 1);
            }
            if (this.multipleSelectedRows.length === 1) {
                this.$emit('oneRowCheck', this.multipleSelectedRows[0]);
            }
        },
        addCheckboxes: function () {
            if (this.checkingRow) {
                this.headers.unshift(
                    {
                        label: '',
                        field: 'choice',
                        sorting: false,
                        type: 'checkbox',
                        clickable: true

                    },
                );
            }
        },
        getSelectedRow: function (ev) {
            if (ev.target.className.includes('unclickable')) {
                this.$emit('rowClick', ev.currentTarget.id);
            }
        },
        getSelectFields: function () {
            // get the "watching" columns by filtering from select values
            const col = this.availableCols;
            this.tableColumns = [];
            for (let el = 0; el < col.length; el++) {
                if (col[el].selected) {
                    this.tableColumns.push(col[el].value.toLowerCase());
                }
            }
        },
    },
    watch: {
        tableColumns: function () {
            if (typeof this !== 'undefined') {
                const list = this.tableData.headers;
                if (this.tableColumns.length !== 0) {
                    const rtnList = [];
                    for (let i = 0; i < list.length; i++) {
                        if (this.tableColumns.includes(list[i].field)) {
                            rtnList.push(list[i]);
                        }
                    }
                    this.headers = rtnList;
                    this.addCheckboxes();
                } else {
                    this.headers = list;
                }
            }
        }
    },
    computed: {
        singleButtons: function () {
            return this.buttons.filter(
                btn => !btn.double
            );
        },
        doubleButtons: function () {
            return this.buttons.filter(
                btn => btn.double
            );
        }
    }
};
</script>

<style>
.md-form label {
    color: darkgrey !important;
}

.form-control {
    color: black !important;
}
</style>

<style scoped>
.display_flex {
    display: flex;
}

.checkboxCentering {
    padding: 15px 0px 0px 3px;
}

.md {
    border-radius: 25px;
}

.flex_entry {
    flex: 1;
}

.overflow {
    overflow: visible;
}

.ovfno {
    overflow: hidden;
}

.scrolling {
    overflow-x: auto;
    box-shadow: 0 3px 6px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}

.tableStyle {
    text-align: center;
    margin: auto;
    width: 50%;
    padding: 10px;
    font-size: large;
    table-layout: auto;
}

.table-hover tbody tr:hover {
    background-color: #b3e5fc;
}

th {
    cursor: pointer;
}

.table-striped > tbody > tr:nth-child(2n+1) {
    background-color: red;
}

.center {
    margin: auto;
    width: 65%;
    padding: 0px;
}
</style>
