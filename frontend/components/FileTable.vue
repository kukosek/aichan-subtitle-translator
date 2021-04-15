<style scoped>
.container
{ width: 100%;
	   max-width: 680px; /* 800 */
	   text-align: center;
margin: 0 auto;
}

.container h1
{
	font-size: 42px;
	font-weight: 300;
color: #000000;
	   margin-bottom: 40px;
}
.container h1 a:hover,
	.container h1 a:focus
{
color: #000000;
}

.container nav
{
	margin-bottom: 40px;
}
.container nav a
{
	border-bottom: 2px solid #c8dadf;
display: inline-block;
padding: 4px 8px;
margin: 0 5px;
}
.container nav a.is-selected
{
	font-weight: 700;
color: #000000;
	   border-bottom-color: currentColor;
}
.container nav a:not( .is-selected ):hover,
	.container nav a:not( .is-selected ):focus
{
	border-bottom-color: #000000;
}

.container footer
{
color: #000000;
	   margin-top: 40px;
}
.container footer p + p
{
	margin-top: 1em;
}
.container footer a:hover,
	.container footer a:focus
{
color: #000000;
}

.box
{
	font-size: 1.25rem; /* 20 */
position: relative;
padding: 10px 20px;
height: 350px;
}

.files {

height: 320px;
margin: 10px 0px 15px 0px;
overflow-x: hidden;
overflow-y: auto;
}

.box.has-advanced-upload
{
outline: 2px dashed #92b0b3;
		 outline-offset: -10px;

		 -webkit-transition: outline-offset .15s ease-in-out, background-color .15s linear;
transition: outline-offset .15s ease-in-out, background-color .15s linear;
}
.box.is-dragover
{
	outline-offset: -20px;
	outline-color: #000000;
}
.box__dragndrop,
	.box__icon
{
display: none;
}
.box.has-advanced-upload .box__dragndrop
{
display: inline;
}
.box.has-advanced-upload .box__icon
{
width: 100%;
height: 80px;
fill: #3C3C3C;
display: block;
		 margin-bottom: 40px;
}

.box__input {
	background-image: url(~/static/klipartz.com.png);
	background-position-x: right;
	background-repeat: no-repeat;
}

.box.is-uploading .box__input,
	.box.is-success .box__input,
	.box.is-error .box__input
{
visibility: hidden;
}

.box__uploading,
	.box__success,
	.box__error
{
display: none;
}
.box.is-uploading .box__uploading,
	.box.is-success .box__success,
	.box.is-error .box__error
{
display: block;
position: absolute;
top: 50%;
right: 0;
left: 0;

	  -webkit-transform: translateY( -50% );
transform: translateY( -50% );
}
.box__uploading
{
	font-style: italic;
}
.box__success
{
	-webkit-animation: appear-from-inside .25s ease-in-out;
animation: appear-from-inside .25s ease-in-out;
}
@-webkit-keyframes appear-from-inside
{
	from	{ -webkit-transform: translateY( -50% ) scale( 0 ); }
	75%		{ -webkit-transform: translateY( -50% ) scale( 1.1 ); }
	to		{ -webkit-transform: translateY( -50% ) scale( 1 ); }
}
@keyframes appear-from-inside
{
	from	{ transform: translateY( -50% ) scale( 0 ); }
	75%		{ transform: translateY( -50% ) scale( 1.1 ); }
	to		{ transform: translateY( -50% ) scale( 1 ); }
}

.box__restart
{
	font-weight: 700;
}
.box__restart:focus,
	.box__restart:hover
{
color: #000000;
}

.js .box__file
{
width: 0.1px;
height: 0.1px;
opacity: 0;
overflow: hidden;
position: absolute;
		  z-index: -1;
}
.js .box__file + label
{
	max-width: 80%;
	text-overflow: ellipsis;
	white-space: nowrap;
cursor: pointer;
display: inline-block;
overflow: hidden;
}
.js .box__file + label:hover strong,
	.box__file:focus + label strong,
	.box__file.has-focus + label strong
{
color: #000000;
}
.js .box__file:focus + label,
	.js .box__file.has-focus + label
{
outline: 1px dotted #000;
outline: -webkit-focus-ring-color auto 5px;
}
.js .box__file + label *
{
	/* pointer-events: none; */ /* in case of FastClick lib use */
}

.no-js .box__file + label
{
display: none;
}

.no-js .box__button
{
display: block;
}
.box__button
{
	font-weight: 700;
color: #000000;
	   background-color: #000000;
display: none;
padding: 8px 16px;
margin: 40px auto 0;
}
.box__button:hover,
	.box__button:focus
{
	background-color: #000000;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity .5s
}

.fade-enter,
.fade-leave-to {
    opacity: 0
}

.list-item {
}
.list-enter-active, .list-leave-active {
  transition: all 1s;
}
.list-enter, .list-leave-to /* .list-leave-active below version 2.1.8 */ {
  opacity: 0;
  transform: translateY(30px);
}
</style>
<template>
	<CBox class="container" role="main"
			v-bind="mainStyles[colorMode]">
		<form
			class="box"
			v-bind:class="{ 'has-advanced-upload': isAdvancedUpload, 'is-dragover': dragOver}"
			v-on:dragover="dragOver=true" v-on:dragenter="dragOver=true"
			v-on:dragleave="dragOver=false" v-on:dragend="dragOver=false"
			@drop.prevent="onDrop" @dragover.prevent
		>
			<transition name="fade" mode="out-in">
				<c-flex key=1 direction="column" height="100%" justify="center" v-if="!loadedFiles.length" class="box__input">
					<c-flex direction="row" align="center">
						<c-icon size="64px" name="download"/>
						<div>
							<strong><a role="button" @click="$refs.fileInput.click()">
							Choose a file
							</a></strong><span class="box__dragndrop"> or drag it here</span>.
						</div>
					</c-flex>

					<input @change="onFileInputChange" type="file" ref="fileInput" v-show="!isAdvancedUpload" name="files[]" id="file" class="box__file" data-multiple-caption="{count} files selected" multiple />
					<button type="submit" class="box__button">Upload</button>
				</c-flex>
				<CBox key=2 v-else class="files">
					<transition-group name="list">
						<c-stack :spacing="3" v-for="(item, x) in loadedFiles" :key="`key-${x}`" class="list-item" >
							<FileTranslateView
							:fileName="item.fileName"
							:fileContents=item.fileContent
							:fileFormat=item.fileFormat
							:srcLangCode=srcLangCode
							:tgtLangCode=tgtLangCode
							@result="onResultUpdate"
							/>
						</c-stack>
					</transition-group>
				</CBox>
			</transition>

		</form>
		<transition name="fade">
			<c-button
				@click="downloadAll()"
				variant-color="blue"
				left-icon="download"
				size="md"
				v-if="loadedFiles.length > 1"
				:disabled="!everythingTranslated"
			>
				Download all
			</c-button>
		</transition>
	</CBox>

</template>
<script lang="ts">
	import { Prop, Watch, Component, Vue , Inject} from 'vue-property-decorator'
	import FileTranslateView from '../components/FileTranslateView.vue'
	import JSZip from 'jszip'
	import { saveAs } from 'file-saver';
	interface FileStore {
		fileName: string;
		fileFormat: string;
		fileContent: string;
		result: string;
	}
		interface ResultPass {
			fileName: string;
			result: string;
		}
	@Component({
		components: {
			FileTranslateView,
		}
	})
	export default class FileTable extends Vue {
		@Prop(String) srcLangCode!: string;
		@Prop(String) tgtLangCode!: string;
		private loadedFiles: FileStore[] = []
		private showBadFormat: Boolean = false
		private isAdvancedUpload: Boolean = true
		private dragOver: Boolean = false
		private numOfTranslated = 0
		private mainStyles: Object = {
			dark: {
			  bg: 'gray.700',
			  color: 'whiteAlpha.900'
			},
			light: {
			  bg: 'white',
			  color: 'gray.600'
			}
		  }
		@Inject('toast') private toast!: (props: Object) => void
		@Inject('$chakraColorMode') private chakraColorMode!: () => string
		@Inject('$toggleColorMode') private toggleColorMode!: () => void


		@Watch('srcLangCode')
		onPropertyChanged(value: string, oldValue: string) {
			this.numOfTranslated = 0
		}


		@Watch('tgtLangCode')
		onTgtLangChanged(value: string, oldValue: string) {
			this.numOfTranslated = 0
		}

		get colorMode(): string {
		  return this.chakraColorMode()
		}

		get everythingTranslated() : Boolean {
			return this.numOfTranslated == this.loadedFiles.length
		}

		public onResultUpdate(value: ResultPass) {
			this.numOfTranslated++;
			this.loadedFiles.forEach(item => {
				if (item.fileName == value.fileName) {
					item.result = value.result
				}
				})
		}

		public onFilesAdded(files: FileList) : void {
			for (var i = 0; i < files.length; i++) {
				const file : File = files[i];
				const fileNameSplitted = file.name.split('.')
				const fileExtension : string = fileNameSplitted[fileNameSplitted.length-1]

				const toast = this.toast
				if(!(['ass', 'srt'].includes(fileExtension))) {
					this.toast({
						title: 'Unsupported file format.',
						description: "We only support .ass and .srt.",
						status: 'error',
						duration: 5000,
						isClosable: true
					})
				}else{
					var reader = new FileReader();
					reader.readAsText(file, "UTF-8");

					var loadedFiles : FileStore[] = this.loadedFiles
					reader.onload = function (e) {
						const content = e!.target!.result;
						loadedFiles.push({fileName: file.name, fileFormat: fileExtension, fileContent: content, result: ""} as FileStore)
					}
					reader.onerror = function (e) {
						toast({
							title: 'Error occurred during reading',
							description: "Check if file "+file.name+" is in the correct format",
							status: 'error',
							duration: 5000,
							isClosable: true
						})
					}
				}
			}
		}

		public downloadAll() {
			var zip = new JSZip();
			this.loadedFiles.forEach( (item) => {
				const fileNameSplitted : String[] = item.fileName!.split('.')
				fileNameSplitted[fileNameSplitted.length-2] += '_' + this.tgtLangCode.toUpperCase()

				zip.file(fileNameSplitted.join('.'), item.result)
			})
			zip.generateAsync({type:"blob"})
				.then(function(content) {
					// see FileSaver.js
					saveAs(content, "aichan-subs.zip");
				});
		}

		public onFileInputChange(e: InputEvent) {
			if (e == null ) {
				return
			}
			if ((e.target as HTMLInputElement).files && (e!.target as HTMLInputElement).files!.length) {
				const addedFiles : FileList = (e.target as HTMLInputElement).files as FileList
				this.onFilesAdded(addedFiles)
			}
		}

		public onDrop(e: DragEvent | undefined | null) : void {
			this.dragOver = false
			if (e == null) {
				return
			}
			e.preventDefault()
			const droppedFiles : FileList = e!.dataTransfer!.files; // the files that were dropped
			this.onFilesAdded(droppedFiles)
		}
		mounted() {
			if (process.client) {
			// feature detection for drag&drop upload
				this.isAdvancedUpload = function()
					{
						var div = document.createElement( 'div' );
						return ( ( 'draggable' in div ) || ( 'ondragstart' in div && 'ondrop' in div ) ) && 'FormData' in window && 'FileReader' in window;
					}();


			}
		}
	}
</script>

