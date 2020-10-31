<template>
	<div>
		<button
			v-if="!primaryToSecondary"
			@click="$emit('click', button.primaryName)"
			type="button"
			:disabled="disabled"
			class="btn btn-outline-white btn-rounded btn-md px-2"
		>
            <span
            >{{button.primaryLabel}}
            </span>
			<mdb-icon class="fas mx-1" :icon="button.primaryIcon"/>
		</button>
		<button
			v-if="primaryToSecondary"
			@click="$emit('click', button.secondaryName)"
			type="button"
			:disabled="disabled"
			class="btn btn-outline-white btn-rounded btn-md px-2"
		>
			<span>{{button.secondaryLabel}}</span>
			<mdb-icon class="fas mx-1" :icon="button.secondaryIcon"/>
		</button>
	</div>
</template>

<script>
	export default {
		props: {
			primaryToSecondary: Boolean,
			disabled: Boolean,
			button: Object
		},
		data: function () {
			return {};
		},
		mounted: function () {
		},
	};
</script>
<style scoped>

</style>
