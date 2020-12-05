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
            this.$axios.get('/user')
                .then(res => {
                    this.private.userData.fetched = true;
                    this.private.userData.data = res.data;
                    let routes = [];
                    if (res.data.roles[0].name === 'admin') {
                        routes = routes.concat(require('./router/Admin').default);
                    }
                    else if (res.data.roles[0].name === 'member') {
                        routes = routes.concat(require('./router/User').default);
                    }
                    else if (res.data.roles[0].name === 'owner')  {
                        routes = routes.concat(require('./router/Owner').default);
                    }
                    this.$router.addRoutes(routes);
                    this.$root.routes = this.$root.routes.concat(routes);
                    if (callback) callback();
                })
                .catch();
        },
        initAxiosHeaders: function (cred) {
            const accessToken = this.$session.get('access');
            if (accessToken) {
                this.$axios.defaults.headers.common.Authorization = 'Bearer ' + accessToken;
                let headers= {
                    'Content-Type': 'application/json',
                }
                this.$axios.post(
                    '/v1/auth/tokens',
                    JSON.stringify({"name":cred.username,"password":cred.password}) ,
                    {headers: headers}
                    )
                .then(res => {
                    this.$axios.defaults.headers.common.Xtoken = res.headers['x-subject-token'];
                })
                .catch(e => {
                    console.log(e)
                })

            }
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
        return '309984b0-3222-4da8-8208-c41846483079'
};

Vue.prototype.$getClient_secret = function () {
        return '1764b99a-dead-4ec1-8a6e-2a5bf774c059'
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
            title: 'Προσοχη!',
            text: message,
            duration: notificationDuration,
            type: 'warning'
        });
    }

}
vm.$mount('#app');
