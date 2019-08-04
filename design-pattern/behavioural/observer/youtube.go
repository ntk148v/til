package main

import "fmt"

type Observer interface {
	update(interface{})
}

type Subject interface {
	registerObserver(obs Observer)
	removeObserver(obs Observer)
	notifyObserver()
}

type Video struct {
	title string
}

// YoutubeChannel is a concrete implementation of Subject interface
type YoutubeChannel struct {
	Observers []Observer
	NewVideo  *Video
}

// notify to all observers when a new video is released
func (yt *YoutubeChannel) notifyObservers() {
	for _, obs := range yt.Observers {
		obs.update(yt.NewVideo)
	}
}

func (yt *YoutubeChannel) ReleaseNewVideo(video *Video) {
	yt.NewVideo = video
	yt.notifyObservers()
}

// UserInterface is a conrete implementation of Observer interface
type UserInterface struct {
	UserName string
	Videos   []*Video
}

func (ui *UserInterface) update(video interface{}) {
	ui.Videos = append(ui.Videos, video.(*Video))
	for video := range ui.Videos {
		View.AddChildNode(NewVideoComponent(video))
	}
	fmt.Printf("UI %s - Video: '%s' has just been released\n", ui.UserName, video.(*Video).title)
}

func main() {
	var ytChannel Subject = &YoutubeChannel{}
	ui1 := NewUserInterface("Bob")
	ui2 := NewuserInterface("Peter")
	ytChannel.registerObserver(ui1)
	ytChannel.registerObserver(ui2)
	ytChannel.(*YoutubeChannel).ReleaseNewVideo(&Video{title: "Avatar 2 trailer"})
	ytChannel.(*YoutubeChannel).ReleaseNewVideo(&Video{title: "Avengers Endgame trailer"})
}
