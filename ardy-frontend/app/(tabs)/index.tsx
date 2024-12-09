import React from 'react';
import { Text, View, ScrollView, Image, FlatList, Dimensions } from 'react-native';
import { styles } from './index_styles';
import Stories from '@/components/stories';
import { Rating } from 'react-native-ratings';
import Carousel from '@/components/carousel';

const logoImage = require('@/assets/images/logo.png');

// Mock data for reviews
const reviews = [
  { id: 1, text: "Amazing Service!", rating: 3, username: "John Doe", serviceprovider: "Consultant" },
  { id: 2, text: "Very professional team.", rating: 4, username: "Jane Smith", serviceprovider: "Construction" },
  { id: 3, text: "Highly recommend Ardy.", rating: 5, username: "Alex Lee", serviceprovider: "Interior Designer" },
  { id: 4, text: "Best Support Ever.", rating: 5, username: "Alex Lee", serviceprovider: "Smart Home" },
];

// Mock data for service providers
const serviceProviders = [
  { name: 'Consultant', logo: require('@/assets/images/logo.png') },
  { name: 'Construction Company', logo: require('@/assets/images/logo.png') },
  { name: 'Interior Designer', logo: require('@/assets/images/logo.png') },
  { name: 'Smart Home Services', logo: require('@/assets/images/logo.png') },
];

// Mock data for carousel images
const carouselImages = [
  {
    id: '1',
    image: { uri: 'https://via.placeholder.com/400x200.png?text=Latest+Construction+Projects' },
    caption: 'Latest Construction Projects',
  },
  {
    id: '2',
    image: { uri: 'https://via.placeholder.com/400x200.png?text=Modern+Interior+Designs' },
    caption: 'Modern Interior Designs',
  },
  {
    id: '3',
    image: { uri: 'https://via.placeholder.com/400x200.png?text=Smart+Home+Innovations' },
    caption: 'Smart Home Innovations',
  },
];

// Get screen width for proper carousel rendering
const { width } = Dimensions.get('window');

export default function Index() {
  return (
    <ScrollView contentContainerStyle={styles.container}>
      {/* Stories Section */}
      <View style={styles.sliderSection}>
        <View style={styles.sectionTitleWrapper}>
          <Text style={styles.sectionTitle}>Success</Text>
          <Text style={styles.sectionTitleAccent}> Stories</Text>
        </View>
        <Stories />
      </View>

      {/* Marketing and News Carousel */}
        <Carousel
        title= "Latest"
        subtitle="News & Updates"
        data={carouselImages}
        />

      {/* Service Providers Slider */}
      {serviceProviders.length > 0 ? (
        <View style={styles.sliderSection}>
          <View style={styles.sectionTitleWrapper}>
            <Text style={styles.sectionTitle}>Featured</Text>
            <Text style={styles.sectionTitleAccent}> Service Providers</Text>
          </View>
          <FlatList
            data={serviceProviders}
            horizontal
            showsHorizontalScrollIndicator={false}
            keyExtractor={(item, index) => index.toString()}
            renderItem={({ item }) => (
              <View style={styles.card}>
                <Image source={item.logo} style={styles.providerLogo} />
                <Text style={styles.cardText}>{item.name}</Text>
              </View>
            )}
          />
        </View>
      ) : (
        <Text style={styles.placeholder}>No Service Providers Available</Text>
      )}

      {/* Customer Reviews Slider */}
      {reviews.length > 0 ? (
        <View style={styles.sliderSection}>
          <View style={styles.sectionTitleWrapper}>
            <Text style={styles.sectionTitle}>Customer</Text>
            <Text style={styles.sectionTitleAccent}> Reviews</Text>
          </View>
          <FlatList
            data={reviews}
            horizontal
            showsHorizontalScrollIndicator={false}
            keyExtractor={(item) => item.id.toString()}
            renderItem={({ item }) => (
              <View style={styles.card}>
                <Text style={styles.cardText}>"{item.text}"</Text>
                <Text style={styles.username}>"{item.serviceprovider}"</Text>
                <View style={styles.ratingContainer}>
                  <Rating
                    type="custom"
                    ratingCount={5}
                    imageSize={18}
                    startingValue={item.rating}
                    readonly
                    tintColor="#413934ee"
                    style={styles.stars}
                  />
                </View>
                <Text style={styles.username}>- {item.username}</Text>
              </View>
            )}
          />
        </View>
      ) : (
        <Text style={styles.placeholder}>No Reviews Available</Text>
      )}

      {/* Our Services Section */}
      <View style={styles.servicesSection}>
        <View style={styles.sectionTitleWrapper}>
          <Text style={styles.sectionTitle}>Our</Text>
          <Text style={styles.sectionTitleAccent}> Services</Text>
        </View>
        {['Hassle Free', 'Interior Design', 'Consultation', 'Smart Home'].map((service, index) => (
          <View key={index} style={styles.serviceCard}>
            <Text style={styles.serviceTitle}>{service}</Text>
            <Text style={styles.serviceDescription}>
              {service === 'Hassle Free'
                ? 'Innovative journey for building smarter.'
                : service === 'Interior Design'
                ? 'Modern and aesthetic designs tailored to your needs.'
                : service === 'Consultation'
                ? 'Expert advice to guide you from land to living.'
                : 'Enjoy our variety of smart home services.'}
            </Text>
          </View>
        ))}
      </View>
    </ScrollView>
  );
}
