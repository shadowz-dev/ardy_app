import React from 'react';
import { Text, View, StyleSheet, ScrollView, Image } from 'react-native';
import { Rating } from 'react-native-ratings';

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
  return (
    <ScrollView contentContainerStyle={styles.container}>
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

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#2d363b',
    paddingBottom: 20,
  },
  header: {
    flexDirection: 'row', // Align logo and welcome container in a row
    alignItems: 'center', // Vertically align content
    padding: 10,
    marginTop: 10,
    marginBottom: 30, // Add spacing between header and next section
  },
  logoContainer: {
    marginRight: 10, // Add space between the logo and welcome text
  },
  logo: {
    width: 70,
    height: 70,
    borderRadius: 10,
  },
  welcomeContainer: {
    flex: 1, // Take remaining space
  },
  titleWrapper: {
    flexDirection: 'row', // Align title and titleAccent horizontally
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
  },
  titleAccent: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#8ee7e4',
  },
  subtitle: {
    fontSize: 14,
    color: '#fff',
    marginTop: 5,
  },
  sliderSection: {
    marginTop: 20,
    paddingHorizontal: 10,
  },
  sectionTitleWrapper: {
    flexDirection: 'row', // Align main and accent title horizontally
    marginBottom: 10, // Add spacing below the title
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
  sectionTitleAccent: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#8ee7e4',
  },
  slider: {
    flexDirection: 'row',
  },
  card: {
    backgroundColor: '#615e5c3c',
    borderRadius: 8,
    padding: 20,
    marginRight: 15,
    alignItems: 'center',
    justifyContent: 'flex-start',
    width: 150,
    height: 150,
  },
  cardText: {
    color: '#fff',
    fontSize: 14,
    textAlign: 'center',
    marginBottom: 10,
  },
  stars: {
    backgroundColor: 'transparent',
    marginBottom: 10,
  },
  username: {
    color: '#ccc',
    fontSize: 12,
    fontStyle: 'italic',
    textAlign: 'center',
  },
  servicesSection: {
    marginTop: 20,
    paddingHorizontal: 15,
  },
  serviceCard: {
    backgroundColor: '#615e5c3c',
    borderRadius: 8,
    padding: 20,
    marginBottom: 15,
    shadowOpacity: 0.5,
    shadowRadius: 5,
  },
  serviceTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 5,
  },
  serviceDescription: {
    fontSize: 14,
    color: '#ddd',
  },
  ratingContainer: {
    marginBottom: 5,
  },
  providerLogo: {
    width: 70,
    height: 70,
    borderRadius: 35, // Make the logo circular
    marginBottom: 10, // Space between logo and name
  },
});
