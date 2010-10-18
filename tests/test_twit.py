from lib.belle import Belle
b = Belle()
faves = b.GetFavorites('poeks',page=2)

for fave in faves:
	print fave.user.screen_name