import React, { Component } from 'react';
import File from './../File/File';
import io from '../../helpers/io';
import VideoStatus from '../File/VideoStatus';
import axios, { post } from 'axios';

export default class DropFileInput extends Component {
	constructor(props) {
		super(props);
		
		this.state = {
			chunk_size: 64 * 1024,
			files: [],
			user_lists: [],
			uploading: false,
			sampleDownloadUrl: 'http://localhost:5000/samples/name.csv'
		}

		this.updateUserList = this.updateUserList.bind(this);
		this.handleUploadImage = this.handleUploadImage.bind(this);
		this.uploadFile = this.uploadFile.bind(this);
	}

	updateUserList = user_lists => {
		this.setState({
			user_lists: JSON.parse(user_lists)
		})
		// console.log('State: ', this.state);
	}
	
	componentDidMount() {
		var state_current = this;
		io.on('msg', function(data) {
		//   console.log(data.msg)
		  state_current.updateUserList(data.msg);
		});
		
	}


	
	handleUploadImage(ev) {
		ev.preventDefault();
	
		const data = new FormData();
		let file = ev.dataTransfer.files[0];
		console.log(file)
		data.append('file', file);
		data.append('filename', 'this.fileName.value');
		data.append('sid', "22222");
		console.log(data);
		fetch('http://localhost:5000/upload', {
		  method: 'POST',
		  body: data,
		}).then((response) => {
		  console.log(response)
		  // response.json().then((body) => {
		  //   this.setState({ imageURL: `http://localhost:8000/${body.file}` });
		  // });
		});
	}
	
	uploadFile = () => {
		let file = this.state.files[0];
		const data = new FormData();
		data.append('file', file);
		data.append('filename', 'this.fileName.value');
		data.append('sid', "22222");
		console.log(data);
		const url = 'http://localhost:5000/upload';
		const config = {
			headers: {
				'content-type': 'multipart/form-data'
			}
		}
		return  post(url, data , config)
	}

	handlerOnDragOver = event => {
		event.preventDefault();
	};
	
	handlerOnDrop = event => {
		/*
		* Prevent add repeat files to state
		* Add Files to State
		*/
		event.preventDefault();
		
		const array_files = [];
		
		for (let i = 0; i < event.dataTransfer.files.length; i++) {
			let file = event.dataTransfer.files[i];
				if (!this.state.files.map((n) => n.name).includes(file.name)) {
					array_files.push(file);
				}
		}
		
		this.setState({
			files: [...this.state.files, ...array_files],
			uploading: false
		}, () => {
			this.uploadFile();
		});
	};
	
	toggleUpload = () => {
		this.setState({uploading: !this.state.uploading})
	};

	downloadSampleFile = () => {
		let newPageUrl = this.state.sampleDownloadUrl;
		window.open(newPageUrl, "_blank");
	}
	
	removeFile = (index) => {
		this.setState({
			files: this.state.files.filter((_, i) => i !== index)
		});
	};
	
	openVideo = (newPageUrl) => {
		window.open(newPageUrl, "_blank");
	}

	render() {
		let files = this.state.files.map((file, index) => {
			return <File file={file}
									 key={file.name}
			             chunk_size={this.state.chunk_size}
			             uploading={this.state.uploading}
			             clickRemove={this.removeFile.bind(this, index)}
			/>
		});

		let user_lists = this.state.user_lists.map((user, index) => {
			return <VideoStatus user={user}
								key={user.id}
			/>
		});
		
		return (
			<div>
				<div className="Drop-input" onDragOver={this.handlerOnDragOver} onDrop={this.handlerOnDrop}>
					Drop files here!
				</div>
				<div className="Div-files">
					{/*files*/}
					{user_lists}
				</div>
				<div className="Div-Button">
					<button onClick={this.downloadSampleFile}>
						Download Sample File
					</button>
				</div>
			</div>
		)
	}
}