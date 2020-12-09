<template>
	<mdb-modal id="movieModal" @close="closing" size="xl" class="modal">
		<mdb-modal-header class="w-100 align-items-center">
			<mdb-modal-title class="w-100 align-items-center">
				<mdb-row class="justify-content-center ml-3">
					Ειδοποιήσεις
				</mdb-row>
			</mdb-modal-title>
		</mdb-modal-header>
		<mdb-modal-body class="black-text">
			<form novalidate class="label">
				<mdb-row class="black-text text-center mb-5">
					<mdb-col>
						<b class="mr-3"> Νεότερες</b>
					</mdb-col>
				</mdb-row>
				<div
					v-if="typeof(newer) !== 'undefined'"
					class="black-text justify-content-center " id="form_rows">
					<mdb-row
						v-for="item in newer"
						:key="item.id"
						class="black-text text-center"
					>
						<mdb-col>
							<p style="display:inline" class="mr-3">
								{{ item.movie }} </p>
							<span class="vertical-line"></span>
							<p style="display:inline" class="ml-3"> {{ item.notification }} </p>
						</mdb-col>
					</mdb-row>
				</div>
				<mdb-row class="black-text text-center mb-5 mt-5">
					<mdb-col>
						<b class="mr-3"> Προηγούμενες</b>
					</mdb-col>
				</mdb-row>
				<div
					v-if="typeof(older) !== 'undefined'"
					class="black-text justify-content-center " id="form_rows2">
					<mdb-row
						v-for="item in older"
						:key="item.id"
						class="black-text text-center"
					>
						<mdb-col>
							<b class="mr-3">
								{{ item.movie }} </b>
							<span class="vertical-line"></span>
							<b class="ml-3"> {{ item.notification }} </b>
						</mdb-col>
					</mdb-row>
				</div>
			</form>
		</mdb-modal-body>
	</mdb-modal>
</template>

<script>


export default {
	name: "UserNotifications",
	props: {
		notifications: Array
	},
	data: function () {
		return {
			notificationList: [],
			fetched: false
		}
	},
	mounted: function () {
		this.notificationList = this.$root.notificationList
	},
	methods: {
		closing: function () {
			let notSeen = this.notificationList.filter(item => item.seen === false)
			for (let notf in notSeen) {
				const formData = new FormData();
				formData.append('Type', 'seen');
				const query = '/api/Subscription/' + notSeen[notf].id + '/';
				this.$axios.put(query, formData, {headers: {'Content-Type': 'multipart/form-data'}})
			}
			this.$root.notifEnabled = false;
			const query = '/api/Subscription/?notifications';
			this.$axios.get(query)
				.then(
					subs => {
						if (subs.data.notifications !== this.$root.notificationList) {
							this.$root.notificationList = subs.data.notifications;
						}
					})
				.catch(this.$notifyAction.error);

		}
	},
	computed: {
		older: function () {
			return this.$root.notificationList.filter(item => item.seen === true)
		},
		newer: function () {
			return this.$root.notificationList.filter(item => item.seen === false)
		}
	}
}
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

.vertical-line {
	display: inline-block;
	border-left: 1px solid #000000;
	margin: 0 10px;
	height: 25px;
}
</style>