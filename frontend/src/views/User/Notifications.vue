<template>
	<div class="ml-4 mr-4">
		<mdb-container class="text-center">
			<div class="d-flex justify-content-center ml-5 rcorners">
				<Table
					class="mt-5"
					v-if="fetched"
					:tableTitle="'Ειδοπιήσεις'"
					:tableIcon="'bell'"
					:tableData="tableDat"
				/>
			</div>
		</mdb-container>
	</div>
</template>

<script>

import Table from '../../components/Structure/Table';
import {mdbContainer, Sticky} from 'mdbvue';

export default {
	name: "Notifications",
	directives: {
		sticky: Sticky
	},
	components: {
		Table,
		mdbContainer,
	},
	data: function () {
		return {
			notifications: [],
			fetched: false
		}
	},
	mounted: function () {
		this.getNotifications();
		this.createTableHeaders();
	},
	methods: {
		getNotifications: function () {
			const query = '/api/Subscription/?notifications';
			this.$axios.get(query)
				.then(
					subs => {
						this.notifications = subs.data.notifications;
						this.fetched = true;
					})
				.catch(this.$notifyAction.error);
		},
		createTableHeaders: function () {
			const headers = [];
			headers.push({
				label: "Ειδοποίηση",
				field: "notification",
				sorting: true,
				type: 'string',
				clickable: false
			});
			this.headers = headers;
		},
	},
	beforeRouteLeave(to, from, next) {
		let notSeen = this.notifications.filter( item => item.seen === false )
		for (let notf in notSeen) {
			const formData = new FormData();
            formData.append('Type', 'seen');
			const query = '/api/Subscription/' + notSeen[notf].id + '/';
			this.$axios.put(query, formData, {headers: {'Content-Type': 'multipart/form-data'}})
		}

		next()
	},
	computed: {
		tableDat: function () {
			const tData = {};
			const data = [];
			const notif = this.notifications
			for (let i = 0; i < notif.length; i++) {
				const tmpdict = {};
				tmpdict["notification"] = notif[i].notification;
				if (!notif[i].seen)
					data.push(tmpdict);
			}
			tData.data = data
			tData.headers = this.headers;
			return tData;
		}
	}
}
</script>

<style scoped>

</style>