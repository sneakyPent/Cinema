import Vue from 'vue';
import Router from 'vue-router';


Vue.use(Router);


let routes = [
	{path: '/welcome', name: 'Home', component: require('../views/Home/welcome').default},
];

routes = routes.concat(require('./Auth').default);
// routes = routes.concat(require('./Master').default);
// routes = routes.concat(require('./User').default);

Vue.use(Router)

const router = new Router({
	mode: 'history',
	routes: routes,
	scrollBehavior: function (to, from, savedPosition) {
		if (savedPosition) {
			return savedPosition;
		}
		return {x: 0, y: 0};
	},
	linkActiveClass: 'active'
});

router.beforeEach((to, from, next) => {
	next();
	if (to.name === 'Login' || to.name === 'Register') {
		return;
	}
	if (!Vue.prototype.$session.exists()) {

		if ('at' in to.query) {
			const token = to.query.at;
			delete to.query.at;
			// TODO: maybe remove only at param
			router.push({name: 'Login', query: {next: to.path, at: token }});
		} else {
			router.push({name: 'Login', query: {next: to.fullPath}});
		}
	}
});

export default router;

Vue.use(require('vue-analytics').default, {
	id: 'UA-154936697-1',
	router
});