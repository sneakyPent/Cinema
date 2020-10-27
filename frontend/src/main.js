import Vue from 'vue'
import App from './App.vue'
import router from './router';


Vue.config.productionTip = false

import * as mdbvue from 'mdbvue';
import 'bootstrap-css-only/css/bootstrap.min.css';
import 'mdbvue/lib/css/mdb.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';


for (const component in mdbvue) {
	Vue.component(component, mdbvue[component]);
}

new Vue({
    router: router,
    render: h => h(App),
}).$mount('#app')
