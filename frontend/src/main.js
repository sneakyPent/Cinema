import Vue from 'vue'
import './plugins/axios';
import App from './App.vue'
import router from './router';
import Notifications from 'vue-notification';
import VueHead from 'vue-head';
import VueSession from 'vue-session';

Vue.use(Notifications);
Vue.use(VueHead);
Vue.use(VueSession, {persist: true});

Vue.config.productionTip = false

import * as mdbvue from 'mdbvue';
import 'bootstrap-css-only/css/bootstrap.min.css';
import 'mdbvue/lib/css/mdb.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import translations from './data/myDict.json';


for (const component in mdbvue) {
    Vue.component(component, mdbvue[component]);
}
const privateData = {
    userData: {
        fetched: false,
        data: {}
    },
};

const vm = new Vue({
    el: '#app',
    router: router,
    render: h => h(App),
    data: function () {
        return {
            private: privateData,
            authenticated: this.$session.exists(),
            routes: this.$router.options.routes,
            requestsAwaiting: 0,
        };
    },
    created: function () {
        if (this.$root.authenticated) {
            this.initAxiosHeaders();
        }
    },
    computed: {
        userData: function () {
            if (!this.private.userData.fetched) this.initUserData();
            return this.private.userData.data;
        },
    },
    methods: {
        initUserData: function (callback) {
            const accessToken = this.$session.get('access');
            if (!accessToken) {
                this.$router.push({name: 'Login'});
                return;
            }
            const tokenData = this.$root.parseJwt(accessToken);
            this.$axios.get('http://localhost:8000/api/UserProfile/' + tokenData.user_id + '/')
                .then(res => {
                    this.private.userData.fetched = true;
                    this.private.userData.data = res.data;
                    let routes = [];
                    if (this.private.userData.data.role === 'admin') {
                        routes = routes.concat(require('./router/Admin').default);
                    }
                    else if (this.private.userData.data.role === 'user') {
                        routes = routes.concat(require('./router/User').default);
                    }
                    else if (this.private.userData.data.role === 'owner')  {
                        routes = routes.concat(require('./router/Owner').default);
                    }
                    this.$router.addRoutes(routes);
                    this.$root.routes = this.$root.routes.concat(routes);
                    if (callback) callback();
                })
                .catch();
        },
        initAxiosHeaders: function () {
            const accessToken = this.$session.get('access');
            if (accessToken) {
                this.$axios.defaults.headers.common.Authorization = 'Bearer ' + accessToken;
            }
        },
        parseJwt: function (token) {
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const jsonPayload = decodeURIComponent(
                atob(base64)
                    .split('')
                    .map(function (c) {
                        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                    })
                    .join('')
            );

            return JSON.parse(jsonPayload);
        },
    },
});


Vue.prototype.$datepickerOptions = function () {
	return {
		week: [
			'Δε',
			'Τρ',
			'Τετ',
			'Πεμ',
			'Παρ',
			'Σαβ',
			'Κυρ',
		],
		month: [
			'Ιανουάριος',
			'Φεβρουάριος',
			'Μάρτιος',
			'Απρίλιος',
			'Μάιος',
			'Ιούνιος',
			'Ιούλιο',
			'Αύγουστος',
			'Σεπτέμβριος',
			'Οκώβριος',
			'Νοέμβριος',
			'Δεκέμβριος',
		],
		format: 'YYYY-MM-DD',
	};
};

Vue.prototype.$getClient_id = function () {
        return '2f43e567-2772-41f5-9024-481a4123d812'
};

Vue.prototype.$getClient_secret = function () {
        return '01b24efb-75bb-45e6-85e0-06a70b94e737'
};

Vue.prototype.$tr = function ( message ) {
    if (translations[message] !== undefined)
        return translations[message]
    else
        return message
}


const notificationDuration = 600
Vue.prototype.$notifyAction =  {
     error: message => {
        vm.$notify({
            title: 'Σφάλμα',
            text: message,
            duration: notificationDuration,
            type: 'error'
        });
    },
    success: message => {
        vm.$notify({
            text: message,
            duration: notificationDuration,
            type: 'success'
        });
    },
    warning: message => {
        vm.$notify({
            title: 'Ενημέρωση',
            text: message,
            duration: notificationDuration,
            type: 'warning'
        });
    }

}
vm.$mount('#app');
