<template>
	<div class="ml-5 mr-4">
		<mdb-container class="text-center">
			<hr>
		</mdb-container>
		<div class="d-flex justify-content-center ml-5 rcorners">
			<Table
				v-if="fetched"
				:buttons="tableButtons"
				:tableTitle="'Τανίες'"
				:tableIcon="'film'"
				checkingRow
				clickRow
				:tableData="tableData"
				:availableCols="availableCols"
				@rowClick="selectMovieFromTable($event)"
				@buttonsClick="tableButtonsHandler($event)"
			/>
		</div>
		<movie-modal v-if="modal" :closing="closeModal" v-bind:movieInfo="movieInfo" @submitForm="submit($event[0])"
			:disableChanges="movieModalChangesDisabled" :modalTitle="modalTitle" :decline="decline"/>
	</div>
</template>

<script>

import MovieModal from '../../components/Structure/MovieModal';
import Table from '../../components/Structure/Table';
import {mdbContainer, Sticky} from 'mdbvue';

export default {
	name: "Owner",
	directives: {
		sticky: Sticky
	},
	components: {
		Table,
		MovieModal,
		mdbContainer,
	},
	data: function () {
		return {
			selectedMovie: '',
			availableCols: [],
			tableData: {
				data: []
			},
			modalTitle: '',
			movieModalChangesDisabled: false,
			fetched: false,
			buttonsChange: false,
			moviesList: [],
			modal: false,
			submitAction: 'update',
			movieInfo: {},
			tableButtons: [
				{
					label: 'Διαγραφή',
					name: 'delete',
					id: 1,
					icon: 'times',
					forceEnable: false
				},
				{
					label: 'Προσθήκη',
					name: 'add',
					id: 2,
					icon: 'plus',
					forceEnable: true
				},
			],
		};
	},
	mounted: function () {
		this.getMovies();
		this.getAvailableCols();
	},
	methods: {
		selectMovieFromTable: function (user) {
			this.selectedMovie = Number.parseInt(user);
		},
		tableButtonsHandler: function (el) {
			const [button, rows] = el
			switch (button.name) {
				case 'delete':
					this.deleteMovie(rows);
					break;
				case 'add':
					this.submitAction = 'add';
					this.addMovie();
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
		getMovies: function () {
			const query = '/api/Movie';
			this.$axios.get(query)
				.then(
					usres => {
						this.moviesList = usres.data;
						this.fixingTableData();
					})
				.catch(this.$notifyAction.error);
		},
		openModal: function (movie) {
			this.fillForm(movie);
			this.modal = true;
		},
		closeModal: function () {
			this.movieModalChangesDisabled = false
			this.modal = false;
			this.selectedMovie = '';
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
		postMove: function () {
			const query = '/api/Movie/';
			this.$axios.post(query, this.movieInfo)
				.then(() => {
					this.closeModal()
					this.getMovies();
					this.$notifyAction.success('Η ταινία σας προστέθηκε επιτυχώς!');
				})
				.catch(this.$notifyAction.error);
		},
		deleteMovie: function (movies) {
			for (let i = 0; i < movies.length; i++) {
				this.$axios.delete('/api/Movie/' + movies[i] + '/')
					.then(() => {
						this.getMovies();
						this.$notifyAction.success('Επιτυχής Διαγραφή!')
					})
					.catch(this.$notifyAction.error);
			}
		},
		updateMovie: function () {
			const query = '/api/Movie/' + this.movieInfo.id + '/';
			this.$axios.put(query, this.movieInfo)
				.then(() => {
					this.$notifyAction.success('Επιτυχής Ενημέρωση ταινίας!')
					this.getMovies();
					this.closeModal();

				})
				.catch(this.$notifyAction.error);
		},
		submit: function (mInfo) {
			this.movieInfo.id = mInfo.id
			this.movieInfo.title = mInfo.title
			this.movieInfo.category = mInfo.category
			this.movieInfo.cinema = mInfo.cinema
			this.movieInfo.startDate = mInfo.startDate
			this.movieInfo.endDate = mInfo.endDate
			switch (this.submitAction) {
				case 'update':
					this.updateMovie()
					break;
				case 'add':
					this.postMove()
					this.submitAction = 'update'
					break;
				default:
					console.log('default');
			}
		},
		decline: function () {
			this.closeModal();
			this.$notifyAction.success('Απόρριψη αλλαγών')
		},
		fillForm: function (movie) {
			this.movieInfo.id = movie.id;
			this.movieInfo.title = movie.title;
			this.movieInfo.category = movie.category;
			this.movieInfo.cinema = movie.cinema;
			this.movieInfo.startDate = movie.startDate;
			this.movieInfo.endDate = movie.endDate;
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
					tmpdict[val[j].value.toLowerCase()] = mList[i][val[j].value];
				}
				data.push(tmpdict);
			}
			// headers.push({label: 'id', field: 'id', sorting: true, type: 'string', clickable: false});
			for (let i = 0; i < val.length; i++) {
				if (!(val[i].value.toLowerCase() === 'id'))
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
	watch: {
		selectedMovie: function () {
			if (this.selectedMovie !== '') {
				let movie = this.moviesList.find(el => {
					if (el.id !== null)
						return el.id === this.selectedMovie;
				})
				this.modalTitle = movie.title;
				this.openModal(movie);
			}
		}
	}
}
;
</script>

<style scoped>


.rcorners {
	border-radius: 25px;
}

</style>