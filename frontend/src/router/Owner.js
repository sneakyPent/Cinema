export default [
	{
		path: '/welcome',
		name: 'Home',
		component: require('../views/Home/welcome').default,
		meta: {
			requiresSession: true
		},
		sidenav: {
			name: 'Αρχική',
			to: '/welcome',
			icon: 'home',
		}
	},
	{
		path: '/owner',
		name: 'Owner',
		component: require('../views/Owner/Owner').default,
		meta: {
			requiresSession: true
		},
		sidenav: {
			name: 'Βιβλιοθήκη ταινιών',
			to: '/Owner',
			icon: 'photo-video',
		}
	},
	{

		path: '/Logout',
		name: 'Logout',
		component: require('../views/Auth/Logout').default,
		meta: {
			requiresSession: true
		},
		sidenav: {
			name: 'Έξοδος',
			to: '/Logout',
			icon: 'sign-out-alt',
		}
	},

];
