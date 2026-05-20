from django.db import models

# TEAM MODEL

class Team(models.Model):

    name = models.CharField(max_length=100, default='')

    logo = models.ImageField(upload_to='teams/', default='default.jpg')

    captain = models.CharField(max_length=100, default='')

    owner = models.CharField(max_length=100, default='')

    description = models.TextField(default='')

    def __str__(self):
        return self.name


# PLAYER MODEL

class Player(models.Model):

    ROLE_CHOICES = (
        ('Batsman', 'Batsman'),
        ('Bowler', 'Bowler'),
        ('All-Rounder', 'All-Rounder'),
        ('Wicket Keeper', 'Wicket Keeper'),
    )

    name = models.CharField(max_length=100, default='')
    age = models.IntegerField(default=18)
    phone = models.CharField(max_length=15, default='')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Batsman')
    address = models.TextField(default='')

    photo = models.ImageField(upload_to='players/', default='default.jpg')
    payment_screenshot = models.ImageField(upload_to='payments/', default='default.jpg')

    def __str__(self):
        return self.name

# MATCH MODEL

# MATCH MODEL

class Match(models.Model):

    team1 = models.CharField(max_length=100)

    team2 = models.CharField(max_length=100)

    match_date = models.DateField()

    time = models.TimeField()

    venue = models.CharField(max_length=200)

    result = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.team1} vs {self.team2}"
    
    # CLUB MEMBER MODEL

class Member(models.Model):

    ROLE_CHOICES = [
        ('President', 'President'),
        ('Secretary', 'Secretary'),
        ('Treasurer', 'Treasurer'),
        ('Member', 'Member'),
    ]

    name = models.CharField(max_length=100)

    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES
    )

    image = models.ImageField(upload_to='members/')

    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name
class GallerySeason(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class GalleryImage(models.Model):

    season = models.ForeignKey(
        GallerySeason,
        on_delete=models.CASCADE,
        related_name='images'
    )

    title = models.CharField(max_length=100)

    image = models.ImageField(upload_to='gallery/')

    def __str__(self):
        return self.title
class Registration(models.Model):

    player_name = models.CharField(max_length=100)

    age = models.IntegerField()

    phone = models.CharField(max_length=15)

    role = models.CharField(max_length=50)

    address = models.TextField()

    photo = models.ImageField(upload_to='registrations/')
    aadhar_card = models.ImageField(upload_to='aadhar/', blank=True, null=True)
    payment_screenshot = models.ImageField(upload_to='payments/')

    

    def __str__(self):
        return self.player_name
    
    # POINTS TABLE MODEL

class PointsTable(models.Model):

    team = models.CharField(max_length=100)

    matches = models.IntegerField(default=0)

    wins = models.IntegerField(default=0)

    losses = models.IntegerField(default=0)

    points = models.IntegerField(default=0)

    nrr = models.FloatField(default=0.0)

    def __str__(self):
        return self.team
    #match result

class Result(models.Model):
    match_name = models.CharField(max_length=200)
    winner = models.CharField(max_length=100)
    man_of_the_match = models.CharField(max_length=100)
    score = models.CharField(max_length=100)
    overs = models.CharField(max_length=50)

    def __str__(self):
        return self.match_name

class Announcement(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title 
    
class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='sponsors/')

    def __str__(self):
        return self.name


 #auction page 
class Auction(models.Model):
    player_name = models.CharField(max_length=100)
    team_name = models.CharField(max_length=100, blank=True, null=True)

    base_price = models.IntegerField(default=1000)
    sold_price = models.IntegerField(default=0)

    is_sold = models.BooleanField(default=False)

    player_image = models.ImageField(upload_to='auction/', blank=True, null=True)

    def __str__(self):
        return self.player_name
    
class Notice(models.Model):

    title = models.CharField(max_length=200)

    file = models.FileField(upload_to='notices/')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title    
