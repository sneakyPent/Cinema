const basePath = '/';

export default [
	{
		path: basePath + 'login',
		name: 'Login',
		component: require('../views/Auth/Login').default
	},
	{
		path: basePath + 'register',
		name: 'Register',
		component: require('../views/Auth/Register').default
	}
];
