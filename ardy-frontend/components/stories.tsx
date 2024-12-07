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
import { Asset } from 'expo-asset';
import * as VideoThumbnails from 'expo-video-thumbnails';

const stories = [
  { id: 1, type: 'image', source: require('@/assets/images/react-logo.png') },
  { id: 2, type: 'image', source: require('@/assets/images/splash.png') },
  { id: 3, type: 'video', source: require('@/assets/videos/sample.mp4') },
  { id: 4, type: 'image', source: require('@/assets/images/Contract.jpg') },
  { id: 5, type: 'image', source: require('@/assets/images/react-logo.png') },
  { id: 6, type: 'image', source: require('@/assets/images/splash.png') },
  { id: 7, type: 'image', source: require('@/assets/images/Contract.jpg') },
];

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

export default function Stories() {
  const [currentStoryIndex, setCurrentStoryIndex] = useState(0);
  const [modalVisible, setModalVisible] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [thumbnails, setThumbnails] = useState<string[]>([]);
  const progressBars = useRef(stories.map(() => new Animated.Value(0))).current;
  const [videoDuration, setVideoDuration] = useState(5000); // Default duration for images

  const videoRef = useRef<Video | null>(null);
  const animationRef = useRef<Animated.CompositeAnimation | null>(null);
  const pausedProgress = useRef<number>(0); // Store progress value when paused

  /**
   * Generate thumbnails for video stories.
   */
  const generateThumbnails = async () => {
    const thumbnailUris = await Promise.all(
      stories.map(async (story) => {
        if (story.type === 'video') {
          try {
            const { uri } = await VideoThumbnails.getThumbnailAsync(
              Asset.fromModule(story.source).uri,
              { time: 1000 }
            );
            return uri;
          } catch (e) {
            console.error('Thumbnail Error:', e);
            return 'https://via.placeholder.com/80';
          }
        } else {
          return Image.resolveAssetSource(story.source).uri;
        }
      })
    );
    setThumbnails(thumbnailUris);
  };

  /**
   * Start or resume progress animation.
   */
  const startProgress = (index: number, duration: number = 5000) => {
    // Reset progress for the current story
    resetProgress(index);
  
    // Start fresh progress animation
    animationRef.current = Animated.timing(progressBars[index], {
      toValue: 1,
      duration,
      useNativeDriver: false,
    });
  
    animationRef.current.start(({ finished }) => {
      if (finished) {
        nextStory(); // Go to next story when animation completes
      }
    });
  };
  
  const pauseProgress = () => {
    if (animationRef.current) {
      animationRef.current.stop();
      progressBars[currentStoryIndex].stopAnimation((value) => {
        pausedProgress.current = value; // Store paused progress
      });
    }
  };
  
  const resumeProgress = () => {
    const remainingDuration = videoDuration * (1 - pausedProgress.current);
    startProgress(currentStoryIndex, remainingDuration);
  };

  const resetProgress = (index: number) => {
    if (progressBars[index]) {
      progressBars[index].stopAnimation();
      progressBars[index].setValue(0); // Reset progress bar value
    }
    pausedProgress.current = 0; // Reset paused progress value
  };

  const resetAllProgressBars = () => {
    progressBars.forEach((bar) => {
      bar.setValue(0);
    });
  };

  /**
   * Open a story at a specific index.
   */
  const openStory = (index: number) => {
    setCurrentStoryIndex(index);
    setModalVisible(true);
    resetAllProgressBars();
    if (stories[index].type === 'video') {
      setIsPaused(false);
    } else {
      startProgress(index, 5000);
    }
  };

  /**
   * Navigate to the next story.
   */
  // Navigation functions
const nextStory = () => {
    const nextIndex = currentStoryIndex + 1;
    if (nextIndex < stories.length) {
      resetProgress(currentStoryIndex);
      setCurrentStoryIndex(nextIndex);
      if (stories[nextIndex].type === 'video') {
        setIsPaused(false);
      } else {
        startProgress(nextIndex);
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
        setIsPaused(false);
      } else {
        startProgress(prevIndex);
      }
    }
  };
  
  const closeStory = () => {
    setModalVisible(false);
    resetAllProgressBars();
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
            <Image source={{ uri: thumbnails[index] }} style={styles.thumbnailImage} />
          </TouchableOpacity>
        )}
      />

      <Modal visible={modalVisible} transparent animationType="fade">
        <View style={styles.modalContainer}>
        <TouchableWithoutFeedback
            onPressIn={() => {
                setIsPaused(true);
                pauseProgress(); // Pause animation
            }}
            onPressOut={() => {
                setIsPaused(false);
                resumeProgress(); // Resume animation
            }}
            onPress={(e) => {
                const touchX = e.nativeEvent.locationX;
                if (touchX < SCREEN_WIDTH * 0.3) previousStory();
                else if (touchX > SCREEN_WIDTH * 0.7) nextStory();
            }}
            >
            <View style={styles.touchableArea}>
                {stories[currentStoryIndex]?.type === 'video' ? (
                <Video
                    ref={videoRef}
                    source={stories[currentStoryIndex]?.source}
                    style={styles.storyContent}
                    resizeMode={ResizeMode.CONTAIN}
                    shouldPlay={!isPaused}
                    onLoad={(status) => {
                        if (status.isLoaded) {
                          setVideoDuration(status.durationMillis || 5000);
                          startProgress(currentStoryIndex, status.durationMillis || 5000);
                        }
                      }}
                      onPlaybackStatusUpdate={(status) => {
                        if (status.isLoaded && status.didJustFinish) nextStory();
                      }}
                />
                ) : (
                <Image
                    source={stories[currentStoryIndex]?.source}
                    style={styles.storyContent}
                    resizeMode="contain"
                />
                )}
            </View>
            </TouchableWithoutFeedback>


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

          <TouchableOpacity onPress={closeStory} style={styles.closeButton}>
            <Text style={styles.closeText}>X</Text>
          </TouchableOpacity>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { marginTop: 20 },
  storyThumbnail: { marginRight: 10, borderRadius: 10 },
  thumbnailImage: { width: 80, height: 80, borderRadius: 40 },
  modalContainer: { flex: 1, backgroundColor: '#000' },
  touchableArea: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  storyContent: { width: '100%', height: '80%' },
  progressContainer: { position: 'absolute', top: 10, width: '90%', flexDirection: 'row' },
  progressWrapper: { flex: 1, height: 2, marginHorizontal: 2, backgroundColor: '#444' },
  progressBar: { height: 2, backgroundColor: '#fff' },
  closeButton: { position: 'absolute', top: 40, right: 20, zIndex: 1 },
  closeText: { color: '#fff', fontSize: 20 },
});
