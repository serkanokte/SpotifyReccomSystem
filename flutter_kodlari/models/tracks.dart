

class Track {
  final String id;
  final String name;
  final String genres;
  final String artist;
  final double? euclideanDistance;

  Track({required this.id, required this.name, required this.genres, required this.artist,this.euclideanDistance});

  factory Track.fromJson(Map<String, dynamic> json) {
    return Track(
      id: json['id'],
      name: json['name'],
      genres: json['genres'],
      artist: json['artist'],
      euclideanDistance: json.containsKey('euclidean_distance')
          ? json['euclidean_distance'].toDouble()
          : null,
    );
  }
}
