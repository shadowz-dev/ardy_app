import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  StyleSheet,
  FlatList,
  Image,
  TouchableOpacity,
  Modal,
  Dimensions,
  TouchableWithoutFeedback,
  Animated,
  Text,
  ActivityIndicator,
} from 'react-native';
import { Video, ResizeMode, AVPlaybackStatusSuccess } from 'expo-av';
import * as VideoThumbnails from 'expo-video-thumbnails';
import { Asset } from 'expo-asset';

const stories = [
  { id: 1, type: 'image', source: require('@/assets/images/splash.png') },
  { id: 2, type: 'image', source: require('@/assets/images/splash.png') },
  { id: 3, type: 'video', source: Asset.fromModule(require('@/assets/videos/sample.mp4')).uri },
  { id: 4, type: 'image', source: require('@/assets/images/splash.png') },
];

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

export default function Stories() {
  const [currentStoryIndex, setCurrentStoryIndex] = useState(0);
  const [modalVisible, setModalVisible] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [thumbnails, setThumbnails] = useState<string[]>([]);
  const [videoDuration, setVideoDuration] = useState(5000);
  const [isVideoLoading, setIsVideoLoading] = useState(false);
  const progressBars = useRef(stories.map(() => new Animated.Value(0))).current;

  const videoRef = useRef<Video | null>(null);

  const generateThumbnails = async () => {
    const thumbnailUris = await Promise.all(
      stories.map(async (story) => {
        if (story.type === 'video') {
          try {
            const { uri } = await VideoThumbnails.getThumbnailAsync(story.source, { time: 1000 });
            return uri;
          } catch (e) {
            console.error('Thumbnail generation failed:', e);
            return 'https://via.placeholder.com/80'; // Fallback to null if generation fails
          }
        }
        return null;
      })
    );
    setThumbnails(thumbnailUris.map((uri) => (uri ? uri : 'https://via.placeholder.com/80')));
  };

  const openStory = (index: number) => {
    if (index < 0 || index >= stories.length) return;
    setCurrentStoryIndex(index);
    setModalVisible(true);
    resetAllProgressBars();
    startProgress(index);
  };

  const closeStory = () => {
    setModalVisible(false);
    resetAllProgressBars();
  };

  const nextStory = () => {
    const nextIndex = currentStoryIndex + 1;
    if (nextIndex < stories.length) {
      resetProgress(currentStoryIndex);
      setCurrentStoryIndex(nextIndex);
      if (stories[nextIndex].type === 'video') {
        // Wait for video load to start progress
        setIsPaused(true);
      } else {
        // Start progress bar for image
        startProgress(nextIndex, 5000);
      }
    } else {
      closeStory();
    }
  };
  
  const previousStory = () => {
    const prevIndex = currentStoryIndex - 1;
    if (prevIndex >= 0) {
      resetProgress(currentStoryIndex);
      resetProgress(prevIndex);
      setCurrentStoryIndex(prevIndex);
      if (stories[prevIndex].type === 'video') {
        setIsPaused(true);
      } else {
        startProgress(prevIndex, 5000);
      }
    }
  };

  const startProgress = (index: number, duration: number = 5000) => {
    resetProgress(index); // Reset the current progress bar
    Animated.timing(progressBars[index], {
      toValue: 1,
      duration,
      useNativeDriver: false,
    }).start(() => {
      if (modalVisible && currentStoryIndex === index) nextStory(); // Move to the next story when the bar finishes
    });
  };
  
  

  const resetProgress = (index: number) => {
    if (progressBars[index]) {
      progressBars[index].stopAnimation();
      progressBars[index].setValue(0);
    }
  };

  const resetAllProgressBars = () => {
    progressBars.forEach((bar) => {
      bar.stopAnimation();
      bar.setValue(0);
    });
  };

  useEffect(() => {
    generateThumbnails();
  }, []);

  return (
    <View style={styles.container}>
      <FlatList
        data={stories}
        horizontal
        showsHorizontalScrollIndicator={false}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item, index }) => (
          <TouchableOpacity onPress={() => openStory(index)} style={styles.storyThumbnail}>
            {item.type === 'video' && thumbnails[index] ? (
              <Image source={{ uri: thumbnails[index] }} style={styles.thumbnailImage} />
            ) : (
              <Image source={item.source} style={styles.thumbnailImage} />
            )}
          </TouchableOpacity>
        )}
      />

      <Modal visible={modalVisible} transparent={true} animationType="slide">
        <View style={styles.modalContainer}>
          {/* Close Button */}
          <TouchableOpacity onPress={closeStory} style={styles.closeButton}>
            <Text style={styles.closeText}>X</Text>
          </TouchableOpacity>

          <TouchableWithoutFeedback
            onPress={(e) => {
              const touchX = e.nativeEvent.locationX;
              if (touchX < SCREEN_WIDTH / 2) {
                previousStory();
              } else {
                nextStory();
              }
            }}
            onPressIn={() => {
                setIsPaused(true);
                progressBars[currentStoryIndex].stopAnimation(); // Stop progress bar when pausing
              }}
              onPressOut={() => {
                setIsPaused(false);
                progressBars[currentStoryIndex].stopAnimation((currentValue) => {
                  const remainingTime = (1 - currentValue) * videoDuration; // Calculate remaining duration
                  startProgress(currentStoryIndex, remainingTime); // Resume progress bar
                });
              }}
          >
            <View style={styles.touchableArea}>
              {stories[currentStoryIndex]?.type === 'video' ? (
                <>
                {isVideoLoading && <ActivityIndicator size="large" color="#fff" />}
                <Video
                ref={videoRef}
                source={{ uri: stories[currentStoryIndex]?.source }}
                style={[styles.storyContent, { width: SCREEN_WIDTH, height: SCREEN_HEIGHT * 0.8 }]}
                resizeMode={ResizeMode.CONTAIN}
                shouldPlay={!isPaused}
                isMuted={false}
                onLoad={(status) => {
                    if (status.isLoaded) {
                    setVideoDuration(status.durationMillis || 5000); // Update video duration
                    startProgress(currentStoryIndex, status.durationMillis || 5000); // Start progress bar with actual duration
                    } else {
                    console.error('Error loading video:', status.error);
                    }
                }}
                onPlaybackStatusUpdate={(status) => {
                    if (status.isLoaded) {
                    if (status.didJustFinish) {
                        nextStory(); // Automatically move to the next story when the video finishes
                    }
                    }
                }}
                onLoadStart={() => {
                    setIsPaused(true); // Pause until the video is loaded
                }}
                onReadyForDisplay={() => {
                    setIsPaused(false); // Resume playback once the video is ready
                }}
                />
                </>
                ) : (
                <Image
                    source={stories[currentStoryIndex]?.source}
                    style={[styles.storyContent, { width: SCREEN_WIDTH, height: SCREEN_HEIGHT * 0.8 }]}
                    resizeMode="contain"
                />
              )}
            </View>
          </TouchableWithoutFeedback>

          {/* Progress Bar */}
          <View style={styles.progressContainer}>
            {stories.map((_, i) => (
              <View key={i} style={styles.progressWrapper}>
                <Animated.View
                  style={[
                    styles.progressBar,
                    {
                      width: progressBars[i].interpolate({
                        inputRange: [0, 1],
                        outputRange: ['0%', '100%'],
                      }),
                    },
                  ]}
                />
              </View>
            ))}
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginTop: 20,
    paddingHorizontal: 10,
  },
  storyThumbnail: {
    marginRight: 10,
    borderRadius: 10,
    overflow: 'hidden',
  },
  thumbnailImage: {
    width: 80,
    height: 80,
    borderRadius: 40,
  },
  modalContainer: {
    flex: 1,
    backgroundColor: '#000',
  },
  closeButton: {
    position: 'absolute',
    top: 40,
    right: 20,
    zIndex: 1,
    backgroundColor: '#fff',
    borderRadius: 20,
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  closeText: {
    fontSize: 20,
    color: '#000',
  },
  progressContainer: {
    position: 'absolute',
    top: 10,
    width: '90%',
    flexDirection: 'row',
  },
  progressWrapper: {
    flex: 1,
    height: 2,
    backgroundColor: '#aaa',
    marginHorizontal: 2,
  },
  progressBar: {
    height: 2,
    backgroundColor: '#fff',
  },
  touchableArea: {
    flex: 1,
    width: SCREEN_WIDTH,
    justifyContent: 'center',
    alignItems: 'center',
  },
  storyContent: {
    width: '100%',
    height: '80%',
  },
});
