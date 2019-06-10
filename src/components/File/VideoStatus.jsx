import React, { PureComponent } from 'react';
import { Line } from 'rc-progress';
import { readFileChunk, onReadSuccess, onReadError } from '../../actions/';
import io from '../../helpers/io';

export default class VideoStatus extends PureComponent {
	constructor(props) {
		super(props);
	}

	openVideo = () => {
		let newPageUrl = this.props.user.url;
		window.open(newPageUrl, "_blank");
	}
	

	render() {
		let view_btn = ''
		if(this.props.user.url_enabled){
			view_btn = <button className="File-button-remove" onClick={this.openVideo}>View File</button>
		} 

		return (
			<div className="File">
				<span className="File-name">Name: {this.props.user.name}</span>
				<span className="File-type">File Generated: {this.props.user.video_generated.toString() }</span>
				<span className="File-type">Video Sent: {this.props.user.video_sent.toString() }</span>
				<span className="File-type">URL: {this.props.user.url.toString() }</span>
				{view_btn}
			</div>
		)
	}
}