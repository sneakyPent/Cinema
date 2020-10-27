<template>
	<div id="app">
		<main >
			<transition name="fade" mode="out-in">
				<router-view/>
			</transition>
		</main>
	</div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style scoped>
	.centered-block {
		position: absolute;
		left: 50%;
		top: 50%;
		transform: translate(-50%, -50%);
		-webkit-transform: translate(-50%, -50%);
	}

	.loaderAnimation {
		-webkit-animation-iteration-count: infinite;
		animation-iteration-count: infinite;
		-webkit-animation-duration: 1s;
		animation-duration: 1s;
		-webkit-animation-fill-mode: both;
		animation-fill-mode: both;
		-webkit-animation-name: loaderPulse;
		animation-name: loaderPulse;
	}

	@keyframes loaderPulse {
		0% {
			-webkit-transform: scale3d(1, 1, 1);
			transform: scale3d(1, 1, 1);
		}
		50% {
			-webkit-transform: scale3d(1.05, 1.05, 1.05);
			transform: scale3d(1.2, 1.2, 1.2);
		}
		100% {
			-webkit-transform: scale3d(1, 1, 1);
			transform: scale3d(1, 1, 1);
		}
	}

	@media (min-width: 768px) {
		.navbar-placeholder {
			margin-top: 72px !important;
		}
	}

	.navbar-placeholder {
		margin-top: 56px;
	}
</style>

<style>
	:root {
		--w-myColor: #faa;
		--w-myColorTrans: rgba(255, 100, 100, 0.75);
		--w-light-gray: #fafafa;
	}

	.bgMyColor {
		background-color: var(--w-myColor);
	}

	.bgMyColorTrans {
		background-color: var(--w-myColorTrans);
	}

	.bg-blur {
		backdrop-filter: blur(4px);
	}

	.fgMyColor {
		color: var(--w-myColor) !important;
	}

	body {
		background-color: var(--w-light-gray);
	}

	@media (min-width: 768px) {
		.h-100-minus-navbar {
			height: calc(100vh - 72px) !important;
		}
	}

	.h-100-minus-navbar {
		height: calc(100vh - 56px);
	}

	.full-screen-img {
		height: 100vh;
		background-repeat: inherit;
		background-position: center center;
		background-size: cover;
	}

	.full-box-img {
		background-repeat: inherit;
		background-position: center center;
		background-size: cover;
	}

	@keyframes rotating {
		from {
			-ms-transform: rotate(0deg);
			-moz-transform: rotate(0deg);
			-webkit-transform: rotate(0deg);
			-o-transform: rotate(0deg);
			transform: rotate(0deg);
		}
		to {
			-ms-transform: rotate(360deg);
			-moz-transform: rotate(360deg);
			-webkit-transform: rotate(360deg);
			-o-transform: rotate(360deg);
			transform: rotate(360deg);
		}
	}

	.rotating {
		/*background-color: black;*/
		-webkit-animation: rotating 60s linear infinite;
		-moz-animation: rotating 60s linear infinite;
		-ms-animation: rotating 60s linear infinite;
		-o-animation: rotating 60s linear infinite;
		animation: rotating 60s linear infinite;
	}

	.w-icon-myIcon {
		mask: url(/static/app/img/icons/myIcon.svg?v1.0);
	}

	.w-icon {
		display: inline-block;
		width: 2rem;
		height: 2rem;
		mask-size: cover;
	}

	.w-link-no-underline,
	.w-link-no-underline:hover {
		text-decoration: none;
	}

	.w-underline-card-title:hover .w-card-title {
		text-decoration: underline;
	}

	.w-card-title-shadow {
		text-shadow: -1px -1px 0.5rem var(--card-title-shadow),
		1px -1px 0.5rem var(--card-title-shadow),
		-1px 1px 0.5rem var(--card-title-shadow),
		1px 1px 0.5rem var(--card-title-shadow);
	}

	.w-border {
		border: dashed 2px var(--w-green6);
	}

	.w-border-top {
		border-top: dashed 2px var(--w-green6);
	}

	.w-border-right {
		border-right: dashed 2px var(--w-green6);
	}

	.w-border-bottom {
		border-bottom: dashed 2px var(--w-green6);
	}

	.w-border-left {
		border-left: dashed 2px var(--w-green6);
	}

	.w-border-top-0 {
		border-top: none !important;
	}

	.w-border-right-0 {
		border-right: none !important;
	}

	.w-border-bottom-0 {
		border-bottom: none !important;
	}

	.w-border-top-0 {
		border-top: none !important;
	}

	.w-border-left-0 {
		border-left: none !important;
	}

	@media (min-width: 576px) {
		.w-border-sm {
			border: dashed 2px var(--w-green6);
		}

		.w-border-top-sm {
			border-top: dashed 2px var(--w-green6);
		}

		.w-border-right-sm {
			border-right: dashed 2px var(--w-green6);
		}

		.w-border-bottom-sm {
			border-bottom: dashed 2px var(--w-green6);
		}

		.w-border-left-sm {
			border-left: dashed 2px var(--w-green6);
		}

		.w-border-top-sm-0 {
			border-top: none !important;
		}

		.w-border-right-sm-0 {
			border-right: none !important;
		}

		.w-border-bottom-sm-0 {
			border-bottom: none !important;
		}

		.w-border-top-sm-0 {
			border-top: none !important;
		}

		.w-border-left-sm-0 {
			border-left: none !important;
		}
	}

	@media (min-width: 768px) {
		.w-border-md {
			border: dashed 2px var(--w-green6);
		}

		.w-border-top-md {
			border-top: dashed 2px var(--w-green6);
		}

		.w-border-right-md {
			border-right: dashed 2px var(--w-green6);
		}

		.w-border-bottom-md {
			border-bottom: dashed 2px var(--w-green6);
		}

		.w-border-left-md {
			border-left: dashed 2px var(--w-green6);
		}

		.w-border-top-md-0 {
			border-top: none !important;
		}

		.w-border-right-md-0 {
			border-right: none !important;
		}

		.w-border-bottom-md-0 {
			border-bottom: none !important;
		}

		.w-border-top-md-0 {
			border-top: none !important;
		}

		.w-border-left-md-0 {
			border-left: none !important;
		}
	}

	@media (min-width: 992px) {
		.w-border-lg {
			border: dashed 2px var(--w-green6);
		}

		.w-border-top-lg {
			border-top: dashed 2px var(--w-green6);
		}

		.w-border-right-lg {
			border-right: dashed 2px var(--w-green6);
		}

		.w-border-bottom-lg {
			border-bottom: dashed 2px var(--w-green6);
		}

		.w-border-left-lg {
			border-left: dashed 2px var(--w-green6);
		}

		.w-border-top-lg-0 {
			border-top: none !important;
		}

		.w-border-right-lg-0 {
			border-right: none !important;
		}

		.w-border-bottom-lg-0 {
			border-bottom: none !important;
		}

		.w-border-top-lg-0 {
			border-top: none !important;
		}

		.w-border-left-lg-0 {
			border-left: none !important;
		}
	}

	@media (min-width: 1200px) {
		.w-border-xl {
			border: dashed 2px var(--w-green6);
		}

		.w-border-top-xl {
			border-top: dashed 2px var(--w-green6);
		}

		.w-border-right-xl {
			border-right: dashed 2px var(--w-green6);
		}

		.w-border-bottom-xl {
			border-bottom: dashed 2px var(--w-green6);
		}

		.w-border-left-xl {
			border-left: dashed 2px var(--w-green6);
		}

		.w-border-top-xl-0 {
			border-top: none !important;
		}

		.w-border-right-xl-0 {
			border-right: none !important;
		}

		.w-border-bottom-xl-0 {
			border-bottom: none !important;
		}

		.w-border-top-xl-0 {
			border-top: none !important;
		}

		.w-border-left-xl-0 {
			border-left: none !important;
		}
	}

	.cursor-pointer {
		cursor: pointer;
	}

	.d-contents {
		display: contents;
	}
</style>
