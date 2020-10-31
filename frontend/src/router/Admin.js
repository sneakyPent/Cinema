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
		path: '/users',
		name: 'Users',
		component: require('../views/Admin/Administration').default,
		meta: {
			requiresSession: true
		},
		sidenav: {
			name: 'Χρήστες',
			to: '/users',
			icon: 'user-alt',
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
	}


];
