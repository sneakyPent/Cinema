<template>
	<div id="app">
		<main :style="{marginTop: '60px'}">
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
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
