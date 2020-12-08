<template>
    <div class="my-0 mp-0 d-md-inline-flex card p-3 pt-4 card-cascade narrower greyBack ">
        <!--Card image-->
        <mdb-card
            class="greyBack
            gradient-card-header blue-gradient justify-content-around align-items-center text-light d-flex narrower display_flex
             view view-cascade my-1 overflow py-2 mx-3 mb-3 flex-column" style=" width: 1000px">
            <mdb-card-body style=" width: auto">
                <mdb-row class="mt-1">
                    <mdb-col>
                        <div class="flex_entry order-1 order-md-2 flex-grow-1">
                            <mdb-card-title tag="h4" bold class="white-text w-100 mt-1">
                                <mdb-icon class="mx-2" :icon=tableIcon
                                />
                                <span><strong style="font-family:Comic Sans MS;">{{ tableTitle }}</strong></span>
                            </mdb-card-title>
                        </div>
                    </mdb-col>
                </mdb-row>
                <mdb-row class="mt-2">
                    <mdb-col v-if="dynamicallySearch">
                        <div v-if="filters !== undefined"
                             class="flex_entry d-flex flex-wrap  order-3 order-md-1 flex-grow-1 mt-2 mb-2">
                            <div v-for="filter in filters"
                                 :key="filter.id"
                                 :id="filter.id"
                                 class="ml-2 mb-1"
                            >
                                <input
                                    type="text"
                                    class="form-control justify-content-around rcorners"
                                    style="text-align: center"
                                    :placeholder="filter.placeholder"
                                    v-model="filter.value"
                                >
                            </div>
                        </div>
                    </mdb-col>
                    <mdb-col md="10" class="justify-content-center" v-else>
                        <div v-if="filters !== undefined"
                             class="flex_entry d-flex flex-wrap  order-3 order-md-1 flex-grow-1 mt-2 mb-2">
                            <div v-for="filter in filters"
                                 :key="filter.id"
                                 :id="filter.id"
                                 class="ml-2 mb-1 d-flex justify-content-end"
                            >
                                <input
                                    v-if="filter.type === 'text'"
                                    @keyup.enter="$emit('search')"
                                    :id="filter.name"
                                    :ref="filter.name"
                                    type="text"
                                    class="form-control justify-content-around rcorners"
                                    style="text-align: center"
                                    :placeholder="filter.placeholder"
                                    v-model="filter.value"
                                >
                                <mdb-date-picker
                                    :id="filter.type"
                                    :ref="filter.name"
                                    v-if="filter.type === 'date'"
                                    class="datePickerAllign form-control justify-content-around rcorners"
                                    style="text-align: center"
                                    :placeholder="filter.placeholder"
                                    v-model="filter.value"
                                    autoHide
                                    disabledPast
                                    :option="$datepickerOptions()"
                                />
                            </div>
                        </div>
                    </mdb-col>
                    <mdb-col md="2" v-if="!dynamicallySearch && filters !== undefined ">
                        <mdb-row>
                            <mdb-btn
                                class="rounded-circle px-2 align-middle"
                                color="white"
                                size="sm"
                                @click="$emit('search')"
                            >
                                <i class="fa fa-search fa-lg"></i>
                            </mdb-btn>
                            <mdb-btn
                                class="rounded-circle px-2 align-middle "
                                color="white"
                                size="sm"
                                @click="$emit('clear')"
                            >
                                <i class="fa fa-times fa-lg"></i>
                            </mdb-btn>
                        </mdb-row>
                    </mdb-col>
                </mdb-row>
                <mdb-row class="justify-content-between" style=" width:950px">
                    <mdb-col col="4" >
                        <div v-if="buttons !== undefined || doublebutton"
                             class=" flex_entry d-flex justify-content-around order-3 order-md-1 flex-grow-1">
                            <button
                                v-for="btn in singleButtons"
                                :disabled="multipleSelectedRows.length === 0 && !btn.forceEnable"
                                :key="btn.id"
                                :id="btn.id"
                                type="button"
                                @click="() => { $emit('buttonsClick',[ btn, multipleSelectedRows]); multipleSelectedRows = []}"
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
                                    @click="() => { doubleButtonClick($event); multipleSelectedRows = []}"/>
                            </div>
                        </div>
                    </mdb-col>
                    <mdb-col col="4">
                        <div
                            class="flex_entry testing d-flex justify-content-around flex-wrap order-2 order-md-3 flex-grow-1 mb-0">
                            <mdb-select
                                id="fields"
                                v-if="availableCols !== undefined "
                                caretStyle="color: white;"
                                style="white-space: nowrap;color: white;"
                                iconClass="d-flex justify-content-end"
                                color="primary"
                                multiple
                                :visibleOptions="6"
                                :selectAllPlaceholder="'Επιλογή όλων'"
                                @getValue="getSelectFields"
                                :options="fields"
                                :label="'Πεδία'"
                            />
                        </div>
                    </mdb-col>
                </mdb-row>
            </mdb-card-body>
        </mdb-card>
        <!--/Card image-->
        <div class="mx-2 mx-md-3">
            <div class="d-flex justify-content-center" style="background-color: white">
                <div class="scrolling" style="display: inline ">
                    <table class="table table-hover tableStyle ovfno table-bordered mx-auto "
                           style="width: 998px;  overflow-x: hidden">
                        <thead>
                        <th :id="header.field" style="white-space: nowrap;"
                            v-for="header in headers" :key="header.field" scope="col">
                            <mdb-icon class='unclickable' mx-1 v-if="customizeColumns" icon="arrows-alt"/>
                            <span class='unclickable'> <strong> <b> {{ header.label }}</b>  </strong> </span>
                        </th>

                        </thead>
                        <tbody v-if="clickRow">
                        <tr
                            style="white-space: nowrap;"
                            v-on:click="getSelectedRow($event)"
                            v-for="item in tableData.data"
                            :key="item.id"
                            :id="item.id"
                        >
                            <td v-bind:class="{ 'unclickable': true, 'checkboxCentering': header.type === 'checkbox',
												table_icon: header.type === 'btn'}"
                                v-for="header in headers"
                                :key="header.field"
                            >
                                <span class='unclickable' v-if="header.type === 'string'"> {{
                                        item[header.field]
                                    }}</span>
                                <mdb-btn
                                    class="rounded-circle px-2"
                                    color="white"
                                    size="sm"
                                    v-if="header.type === 'btn'"
                                    @click="$emit(header.field,[ item.id])"
                                >
									<i v-if="typeof(item[header.field]) !== 'undefined'" :class="rowButtons[item[header.field]].class">
									</i>
									<i v-else :class="rowButtons[header.field].class"></i>
                                </mdb-btn>
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
                        <tbody v-else>
                        <tr

                            style="white-space: nowrap;"
                            v-for="item in tableData.data"
                            :key="item.id"
                            :id="item.id"
                        >
                            <td v-bind:class="{ 'unclickable': true, 'checkboxCentering': header.type === 'checkbox',
                                                table_icon: header.type === 'btn'}"
                                v-for="header in headers"
                                :key="header.field"
                            >
                                <span class='unclickable' v-if="header.type === 'string'"> {{
                                        item[header.field]
                                    }}</span>
                                <mdb-btn
                                    class="rounded-circle px-2"
                                    color="white"
                                    size="sm"
                                    v-if="header.type === 'btn'"
                                    @click="$emit(header.field,[ item.id])"
                                >
									<i v-if="typeof(item[header.field]) !== 'undefined'" :class="rowButtons[item[header.field]].class">
									</i>
									<i v-else :class="rowButtons[header.field].class"></i>
                                </mdb-btn>
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
        filters: Array,
        dynamicallySearch: Boolean,
        availableCols: Array,
        checkingRow: Boolean,
		//rowButtons emit is their field name rawButton key should be the same with the group name,
		//if you want same button different emit, then rawButton key should be different for each one
		//and the will have the same group
        rowButtons: {},
        clickRow: Boolean,
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
            fields: [],
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
        this.filterSize();
        this.setFields();
    },
    methods: {
        setFields: function () {
            if (this.availableCols !== undefined)
                for (const col of this.availableCols) {
                    if (col.value !== 'id')
                        this.fields.push(col)
                }
        },
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
        filterSize: function () {
            if (this.filters !== undefined) {
                // let input = document.querySelectorAll('input');
                let input = document.querySelectorAll('input');
                for (let i = 0; i < input.length; i++) {
                    input[i].setAttribute('size', input[i].getAttribute('placeholder').length);
                    input[i].setAttribute('style', "text-align:center !important;");
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
    },
    directives: {
        focus: {
            inserted(el) {
                el.focus()
            }
        }
    }
};
</script>

<style>
.greyBack {
    background-color: dimgrey;
}

#fields .md-form {
    margin-top: 0px;
    margin-bottom: 0px;
}

#fields .md-form label {
    color: white !important;
}

#date.mdb-vue-date .datepickbox .md-form {
    margin-bottom: 0px !important;
    margin-top: 8px !important;
}

#date.mdb-vue-date .datepickbox .form-control {
    color: black !important;
    border-bottom-width: 0px !important;
    margin-bottom: 0px !important;
    padding-bottom: 0px !important;
    padding-top: 0px !important;

}
</style>

<style scoped>

.mdb-vue-date .datepickbox .md-form {
    margin-bottom: 0px !important;
    margin-top: 8px !important;
    padding-left: 20px;
}

.datePickerAllign {
    display: inline-block;
    vertical-align: top;
    border-bottom-width: 0px;
    padding-bottom: 0px;
    padding-top: 0px;
    border-top-width: 0px;

}

.table_icon {
    padding-top: 0px;
    /*border-top-width: 0px;*/
    padding-bottom: 0px;
    /*border-bottom-width: 0px;/*/
    /*border-left-width: 0px;*/
    /*border-right-width: 0px;*/
    padding-right: 0px;
    padding-left: 0px;
}

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
    width: 40%;
    padding: 0px;
}
</style>
