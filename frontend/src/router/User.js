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
		path: '/movies',
		name: 'Movies',
		component: require('../views/User/Movies').default,
		meta: {
			requiresSession: true
		},
		sidenav: {
			name: 'Ταινίες',
			to: '/movies',
			icon: 'film',
		}

	},
	{
		path: '/favorites',
		name: 'Favorites',
		component: require('../views/User/Favorites').default,
		meta: {
			requiresSession: true
		},
		sidenav: {
			name: 'Αγαπημένα',
			to: '/favorites',
			icon: 'star',
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