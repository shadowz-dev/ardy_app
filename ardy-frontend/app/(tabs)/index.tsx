import React, { useState, useRef, useEffect } from 'react';
import { Text, View, ScrollView, Image, RefreshControl, Animated, FlatList, TouchableOpacity, Modal } from 'react-native';
import Video from 'react-native-video';
import { useNavigation } from 'expo-router';
import { Rating } from 'react-native-ratings';
import { NativeSyntheticEvent, NativeScrollEvent } from 'react-native';
import { styles } from './index_styles';
import Stories from '@/components/stories';

const logoImage = require('@/assets/images/logo.png');

const reviews = [
  { id: 1, text: "Amazing Service!", rating: 3, username: "John Doe" },
  { id: 2, text: "Very professional team.", rating: 4, username: "Jane Smith" },
  { id: 3, text: "Highly recommend Ardy.", rating: 5, username: "Alex Lee" },
  { id: 4, text: "Best Support Ever.", rating: 5, username: "Alex Lee" },
];

const serviceProviders = [
  { name: 'Consultant', logo: require('@/assets/images/logo.png') },
  { name: 'Construction Company', logo: require('@/assets/images/logo.png') },
  { name: 'Interior Designer', logo: require('@/assets/images/logo.png') },
  { name: 'Smart Home Services', logo: require('@/assets/images/logo.png') },
];

export default function Index() {
  const [refreshing, setRefreshing] = useState(false);
  const [scrollOffset, setScrollOffset] = useState(0);
  const pullDownAnimation = useRef(new Animated.Value(0)).current;
  const spinAnimation = useRef(new Animated.Value(0)).current;

   // Spin animation for logo
  const spin = spinAnimation.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  // Trigger spin animation while refreshing
  useEffect(() => {
    if (refreshing) {
      Animated.loop(
        Animated.timing(spinAnimation, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        })
      ).start();
    } else {
      spinAnimation.stopAnimation(() => spinAnimation.setValue(0));
    }
  }, [refreshing]);
  // handle refresh Logic

  const onRefresh = async () => {
    setRefreshing(true);
    // fetch data
    await new Promise((resolve) => setTimeout(resolve, 2000));
    // update state
    setRefreshing(false);
  };

    // Scroll handler
  const handleScroll = (event: NativeSyntheticEvent<NativeScrollEvent>  ) => {
    const offsetY = event.nativeEvent.contentOffset.y;
    setScrollOffset(offsetY);

    // Update pullDownAnimation only for pull-down gesture
    if (offsetY < 0) {
      pullDownAnimation.setValue(offsetY);
    }
  };

  return (
    <ScrollView
      contentContainerStyle={styles.container}
      onScroll={handleScroll}
      scrollEventThrottle={16}
      refreshControl={
        <RefreshControl
          refreshing={false}
          onRefresh={onRefresh}
          tintColor="transparent" // Hide default spinner
          colors={['transparent']} // For Android
        />
      }
    >
      {/* Custom refresh animation */}
      {(scrollOffset < 0 || refreshing) && (
        <View style={styles.pullDownContainer}>
          <Animated.Image
            source={logoImage}
            style={[styles.refreshLogo, { transform: [{ rotate: spin }] }]}
          />
          <Text style={styles.pullDownText}>
            {refreshing ? 'Refreshing...' : 'Swipe Down to Refresh'}
          </Text>
        </View>
      )}

      {/* Header Section */}
      <View style={styles.header}>
        <View style={styles.logoContainer}>
          <Image source={logoImage} style={styles.logo} />
        </View>
        <View style={styles.welcomeContainer}>
          <View style={styles.titleWrapper}>
            <Text style={styles.title}>Welcome to</Text>
            <Text style={styles.titleAccent}> Ardy!</Text>
          </View>
          <Text style={styles.subtitle}>
            Your All-In-One platform for smart construction and design solutions.
          </Text>
        </View>
      </View>

      {/* Stories */}
      <View style={styles.sliderSection}>
      <View style={styles.sectionTitleWrapper}>
          <Text style={styles.sectionTitle}>Success</Text>
          <Text style={styles.sectionTitleAccent}> Stories</Text>
        </View>
        <Stories />
      </View>

      {/* Service Providers Slider */}
      <View style={styles.sliderSection}>
      <View style={styles.sectionTitleWrapper}>
          <Text style={styles.sectionTitle}>Featured</Text>
          <Text style={styles.sectionTitleAccent}> Service Providers</Text>
        </View>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.slider}>
        {serviceProviders.map((provider, index) => (
          <View key={index} style={styles.card}>
            <Image source={provider.logo} style={styles.providerLogo} />
            <Text style={styles.cardText}>{provider.name}</Text>
          </View>
        ))}
        </ScrollView>
      </View>

      {/* Customer Reviews Slider */}
      <View style={styles.sliderSection}>
  <View style={styles.sectionTitleWrapper}>
    <Text style={styles.sectionTitle}>Customer</Text>
    <Text style={styles.sectionTitleAccent}> Reviews</Text>
  </View>
  <ScrollView 
    horizontal 
    showsHorizontalScrollIndicator={false} 
    contentContainerStyle={{ paddingHorizontal: 10 }}
    style={styles.slider}
  >
    {reviews.map(review => (
          <View key={review.id} style={styles.card}>
            <Text style={styles.cardText}>"{review.text}"</Text>
            <View style={styles.ratingContainer}>
              <Rating
                type="custom"
                ratingCount={5}
                imageSize={18}
                startingValue={review.rating}
                readonly // Prevent users from interacting
                tintColor='#413934ee'
                style={styles.stars}
              />
            </View>
            <Text style={styles.username}>- {review.username}</Text>
          </View>
        ))}
  </ScrollView>
</View>

      {/* Our Services Section */}
      <View style={styles.servicesSection}>
        <View style={styles.sectionTitleWrapper}>
          <Text style={styles.sectionTitle}>Our</Text>
          <Text style={styles.sectionTitleAccent}> Services</Text>
        </View>
        <View style={styles.serviceCard}>
          <Text style={styles.serviceTitle}>Hassle free</Text>
          <Text style={styles.serviceDescription}>
            Innovative journy for building smarter.
          </Text>
        </View>
        <View style={styles.serviceCard}>
          <Text style={styles.serviceTitle}>Interior Design</Text>
          <Text style={styles.serviceDescription}>
            Modern and aesthetic designs tailored to your needs.
          </Text>
        </View>
        <View style={styles.serviceCard}>
          <Text style={styles.serviceTitle}>Consultation</Text>
          <Text style={styles.serviceDescription}>
            Expert advice to guide you from land to living.
          </Text>
        </View>
        <View style={styles.serviceCard}>
          <Text style={styles.serviceTitle}>Smart Home</Text>
          <Text style={styles.serviceDescription}>
            Enjoy from our variaty of smart home services.
          </Text>
        </View>
      </View>
    </ScrollView>
  );
}


